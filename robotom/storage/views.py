# coding=utf-8
import logging
from django.contrib import messages
import requests
import json
from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from requests.exceptions import Timeout
from robotom.settings import STORAGE_EXPERIMENTS_HOST, STORAGE_FRAMES_HOST, STORAGE_FRAMES_INFO_HOST

rest_logger = logging.getLogger('rest_logger')


class ExperimentRecord:
    def __init__(self, record):
        if 'specimen' in record:
            self.specimen = record['specimen']
        else:
            self.specimen = ''
        self.dark_count = record['experiment parameters']['DARK']['count']
        self.dark_exposure = record['experiment parameters']['DARK']['exposure']
        self.experiment_id = record['experiment id']
        if record['finished']:
            self.finished = u'Завершен'
        else:
            self.finished = u'Не завершен'
        if record['experiment parameters']['advanced']:
            self.advanced = u'Продвинутый'
        else:
            self.advanced = u'Стандартный'
        self.data_angle_step = record['experiment parameters']['DATA']['angle step']
        self.data_count_per_step = record['experiment parameters']['DATA']['count per step']
        self.data_step_count = record['experiment parameters']['DATA']['step count']
        self.data_exposure = record['experiment parameters']['DATA']['exposure']
        self.empty_count = record['experiment parameters']['EMPTY']['count']
        self.empty_exposure = record['experiment parameters']['EMPTY']['exposure']


def create_pages(request, results, page):
    record_list = [ExperimentRecord(result) for result in results]

    for i in xrange(2):
        record_list += record_list
    pagin = Paginator(record_list, 1500)

    try:
        records = pagin.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        records = pagin.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = pagin.page(pagin.num_pages)

    return records


def make_info(post_args):
    for arg in post_args:
        rest_logger.debug(u'PostArgs: {} {}'.format(arg, post_args[arg]))
    # Внимание! Быдлокод!
    request = {}

    if post_args['DarkFromCount'] != '':
        request['experiment parameters.DARK.count'] = {}
        request['experiment parameters.DARK.count']['$gte'] = int(post_args['DarkFromCount'])
    if post_args['DarkToCount'] != '':
        if 'experiment parameters.DARK.count' not in request:
            request['experiment parameters.DARK.count'] = {}
        request['experiment parameters.DARK.count']['$lte'] = int(post_args['DarkToCount'])
    if post_args['DarkFromExposure'] != '':
        request['experiment parameters.DARK.exposure'] = {}
        request['experiment parameters.DARK.exposure']['$gte'] = float(post_args['DarkFromExposure'])
    if post_args['DarkToExposure'] != '':
        if 'experiment parameters.DARK.exposure' not in request:
            request['experiment parameters.DARK.exposure'] = {}
        request['experiment parameters.DARK.exposure']['$lte'] = float(post_args['DarkToExposure'])

    if post_args['EmptyFromCount'] != '':
        request['experiment parameters.EMPTY.count'] = {}
        request['experiment parameters.EMPTY.count']['$gte'] = int(post_args['EmptyFromCount'])
    if post_args['EmptyToCount'] != '':
        if 'experiment parameters.EMPTY.count' not in request:
            request['experiment parameters.EMPTY.count'] = {}
        request['experiment parameters.EMPTY.count']['$lte'] = int(post_args['EmptyToCount'])
    if post_args['EmptyFromExposure'] != '':
        request['experiment parameters.EMPTY.exposure'] = {}
        request['experiment parameters.EMPTY.exposure']['$gte'] = float(post_args['EmptyFromExposure'])
    if post_args['EmptyToExposure'] != '':
        if 'experiment parameters.EMPTY.exposure' not in request:
            request['experiment parameters.EMPTY.exposure'] = {}
        request['experiment parameters.EMPTY.exposure']['$lte'] = float(post_args['EmptyToExposure'])

    if post_args['Finished'] == u'Завершен':
        request['finished'] = True
    if post_args['Finished'] == u'Не завершен':
        request['finished'] = False

    if post_args['Advanced'] == u'Да':
        request['experiment parameters.advanced'] = True
    if post_args['Advanced'] == u'Нет':
        request['experiment parameters.advanced'] = False

    if post_args['DataFromExposure'] != '':
        request['experiment parameters.DATA.exposure'] = {}
        request['experiment parameters.DATA.exposure']['$gte'] = float(post_args['DataFromExposure'])
    if post_args['DataToExposure'] != '':
        if 'experiment parameters.DATA.exposure' not in request:
            request['experiment parameters.DATA.exposure'] = {}
        request['experiment parameters.DATA.exposure']['$lte'] = float(post_args['DataToExposure'])
    if post_args['DataFromAngleStep'] != '':
        request['experiment parameters.DATA.angle step'] = {}
        request['experiment parameters.DATA.angle step']['$gte'] = int(post_args['DataFromAngleStep'])
    if post_args['DataToAngleStep'] != '':
        if 'experiment parameters.DATA.angle step' not in request:
            request['experiment parameters.DATA.angle step'] = {}
        request['experiment parameters.DATA.angle step']['$lte'] = int(post_args['DataToAngleStep'])
    if post_args['DataFromCountPerStep'] != '':
        request['experiment parameters.DATA.count per step'] = {}
        request['experiment parameters.DATA.count per step']['$gte'] = int(post_args['DataFromCountPerStep'])
    if post_args['DataToCountPerStep'] != '':
        if 'experiment parameters.DATA.count per step' not in request:
            request['experiment parameters.DATA.count per step'] = {}
        request['experiment parameters.DATA.count per step']['$lte'] = int(post_args['DataToCountPerStep'])
    if post_args['DataFromStepCount'] != '':
        request['experiment parameters.DATA.step count'] = {}
        request['experiment parameters.DATA.step count']['$gte'] = int(post_args['DataFromStepCount'])
    if post_args['DataToStepCount'] != '':
        if 'experiment parameters.DATA.step count' not in request:
            request['experiment parameters.DATA.step count'] = {}
        request['experiment parameters.DATA.step count']['$lte'] = int(post_args['DataToStepCount'])

    rest_logger.debug(u'Текст запроса к базе {}'.format(json.dumps(request)))
    return json.dumps(request)


def storage_view(request):
    # TODO паджинация

    page = request.GET.get('page')
    records = []
    num_pages = 0
    to_show = False

    if request.method == "GET":
        if page is not None:
            to_show = True
    elif request.method == "POST":
        info = make_info(request.POST)
        try:
            answer = requests.post(STORAGE_EXPERIMENTS_HOST, info, timeout=1)
            if answer.status_code == 200:
                experiments = json.loads(answer.content)
                rest_logger.debug(u'Найденные эксперименты: {}'.format(experiments))
                page = 1
                records = create_pages(request, experiments, page)
                if len(records) == 0:
                    messages.error(request, u'Не найдено ни одной записи')
                else:
                    to_show = True
                num_pages = len(experiments) / 15
            else:
                rest_logger.error(u'Не удается найти эксперименты. Код ошибки: {}'.format(answer.status_code))
                messages.error(request, u'Не удается найти эксперименты. Код ошибки: {}'.format(answer.status_code))
        except Timeout as e:
            rest_logger.error(u'Не удается найти эксперименты. Ошибка: {}'.format(e.message))
            messages.error(request, u'Не удается найти эксперименты. Сервер хранилища не отвечает. Попробуйте позже.')
        except BaseException as e:
            rest_logger.error(u'Не удается найти эксперименты. Ошибка: {}'.format(e.message))
            messages.error(request, u'Не удается найти эксперименты. Сервер хранилища не отвечает. Попробуйте позже.')

    return render(request, 'storage/storage_index.html', {
        'caption': 'Хранилище',
        'record_range': records,
        'toShowResult': to_show,
        'pages': xrange(1, num_pages + 1),
        'current_page': page,
    })

class FrameRecord:
    def __init__(self, frame):
        self.num = ""
        self.type = ""
        self.date_time = ""
        self.detector_model = ""
        self.exposure = ""
        self.shutter_open = ""
        self.angle_position = ""
        self.current = ""
        self.voltage = ""
        if "num" in frame:
            self.num = frame["num"]
        if "type" in frame:
            self.type = frame["type"]
        if "frame" in frame:
            if "image_data" in frame["frame"]:
                if "datetime" in frame["frame"]["image_data"]:
                    self.date_time = frame["frame"]["image_data"]["datetime"]
                if "detector" in frame["frame"]["image_data"]:
                    if "model" in frame["frame"]["image_data"]["detector"]:
                        self.detector_model = frame["frame"]["image_data"]["detector"]["model"]
                if "exposure" in frame["frame"]["image_data"]:
                    self.exposure = frame["frame"]["image_data"]["exposure"]
            if "shutter" in frame["frame"]:
                if "open" in frame["frame"]["shutter"]:
                    self.shutter_open = frame["frame"]["shutter"]["open"]
            if "object" in frame["frame"]:
                if "angle position" in frame["frame"]["object"]:
                    self.angle_position = frame["frame"]["object"]["angle position"]
            if "X-ray source" in frame["frame"]:
                if "current" in frame["frame"]["X-ray source"]:
                    self.current = frame["frame"]["X-ray source"]["current"]
                if "voltage" in frame["frame"]["X-ray source"]:
                    self.voltage = frame["frame"]["X-ray source"]["voltage"]


def storage_record_view(request, storage_record_id):
    # TODO
    record = {}
    to_show = True
    try:
        exp_info = json.dumps({"experiment id": storage_record_id})
        experiment = requests.post(STORAGE_EXPERIMENTS_HOST, exp_info, timeout=1)
        if experiment.status_code == 200:
            experiment_info = json.loads(experiment.content)
            rest_logger.debug(u'Страница записи: Данные эксперимента: {}'.format(experiment_info))
            if len(experiment_info) == 0:
                messages.error(request, u'Эксперимент с данным идентификатором не найден')
                to_show = False
            else:
                record = ExperimentRecord(experiment_info[0])
        else:
            rest_logger.error(u'Не удается получить эксперимент. Ошибка: {}'.format(experiment.status_code))
            messages.error(request, u'Не удается получить эксперимент. Ошибка: {}')
            to_show = False
    except Timeout as e:
        rest_logger.error(u'Не удается получить эксперимент. Ошибка: {}'.format(e.message))
        messages.error(request, u'Не удается получить эксперимент. Сервер хранилища не отвечает. Попробуйте позже.')
        to_show = False
    except BaseException as e:
        rest_logger.error(u'Не удается получить эксперимент. Ошибка: {}'.format(e.message))
        messages.error(request, u'Не удается получить эксперимент. Сервер хранилища не отвечает. Попробуйте позже.')
        to_show = False

    frames_list = []
    try:
        frame_info = json.dumps({"exp_id": storage_record_id})
        rest_logger.debug(u'Страница записи: {}'.format(frame_info))
        frames = requests.post(STORAGE_FRAMES_INFO_HOST, frame_info, timeout=1)
        if frames.status_code == 200:
            frames_info = json.loads(frames.content)
            rest_logger.debug(u'Страница записи: Список изображений: {}'.format(frames_info))
            frames_list = [FrameRecord(frame) for frame in frames_info]
        else:
            rest_logger.error(u'Не удается получить список изображений. Ошибка: {}'.format(frames.status_code))
            messages.error(request, u'Не удается получить список изображений. Ошибка: {}'.format(frames.status_code))
            to_show = False
    except Timeout as e:
        rest_logger.error(u'Не удается получить список изображений. Ошибка: {}'.format(e.message))
        messages.error(request,
                       u'Не удается получить список изображений. Сервер хранилища не отвечает. Попробуйте позже.')
        to_show = False
    except BaseException as e:
        rest_logger.error(u'Не удается получить список изображений. Ошибка: {}'.format(e.message))
        messages.error(request,
                       u'Не удается получить список изображений. Сервер хранилища не отвечает. Попробуйте позже.')
        to_show = False

    return render(request, 'storage/storage_record_new.html', {
        "record_id": storage_record_id,
        'caption': 'Запись хранилища номер ' + str(storage_record_id),
        'image_range': xrange(1, 5),  # TODO
        'to_show': to_show,
        'info': record,
        'frames_list': frames_list,
    })
