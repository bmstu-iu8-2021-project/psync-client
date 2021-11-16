# Copyright 2021 Peter p.makretskii@gmail.com
# TODO: json in header
# TODO: json reading
# TODO: files with the same name

from os.path import join
import os
import shutil
from io import BytesIO
from UI.ui_sign_in import sign_in_window
from zipfile import ZipFile
import time


# def get_dict(arc_name, folder):
#     folder = folder[folder.find(':') + 1:]
#     storage = '/home/peter/Study/03_semestr/Coursework/Storage'
#     archive = ZipFile(join(storage, arc_name), 'r')
#     archive_content = {}
#     for file in archive.namelist():
#         archive_content[join('/', file).replace(folder, '')] = time.mktime(
#             tuple(list(archive.getinfo(file).date_time) + [0, 0, 0]))
#     return archive_content
#
#
# def merge_archive(archive_one, archive_two):
#     merged = archive_one.copy()
#     merged.update(archive_two)
#     # unity = ZipFile(join('/home/peter/Study/03_semestr/Coursework/Storage', 'common.zip'), 'w')
#     for file in merged:
#         if file in archive_one and file in archive_two:
#             merged[file] = max(archive_one[file], archive_two[file])
#     # unity.close()
#     return merged
#
#
# def copy_data(old, new):
#     old_archive = ZipFile(old, 'r')
#     new_archive = ZipFile(new, 'w')
#
#     for file in old_archive.namelist():
#         old_archive.extract(file, '/home/peter/Study/03_semestr/Coursework/Storage')
#         # item = (old_archive.open(file))
#         # new_archive.write(item)
#         # print(item)
#         # item.close()
#
#     shutil.rmtree(join('/home/peter/Study/03_semestr/Coursework/Storage/home'))
#     old_archive.close()
#     new_archive.close()


storage = '/home/peter/Study/03_semestr/Coursework/Storage/'


# # во входе 0 - путь к архиву, 1 - путь к архивируему, то есть выбранная папка внутри архива
# # разархивируем архив
# # --
# # сливаем архивы как надо, но еще не архивируем,
# def take_out(current_archive, other_archive):
#     # разархивируем архив текущего пользователя во временную папку, при этом сохраним дату изменения
#     current = ZipFile(current_archive[0], 'r')
#     temp = str(time.time())
#     unzip_with_meta(current_archive[0], join(storage, temp + '/'))
#     current.close()
#
#     # разархивируем архив другого пользрвателя в хранилище
#     other = ZipFile(other_archive[0], 'r')
#     unzip_with_meta(other_archive[0], storage)
#     other.close()
#     # сливаем полученные папки во временную, удаляем остатки другого пользователя
#     for file in os.listdir(join(storage, other_archive[1] + '/')):
#         print(join(storage, other_archive[1], file))
#         # print('-', join(storage, other_archive[1], file),
#         #       join(storage, temp, current_archive[1]), sep='\n')
#         # print(' '.join([storage, other_archive[1], file]), ' '.join([storage, temp, current_archive[1]]), sep='\n')
#         shutil.copy2(join(storage, other_archive[1], file),
#                      join(storage, temp, current_archive[1]))
#
#     # shutil.rmtree(join(storage, other_archive[1][:other_archive[1].find('/')]))
#     print(join(storage, other_archive[1][:other_archive[1].find('/')]))
#
#     # создаем слитый архив и заполняем так, будто идем из корня устройства
#     merged = ZipFile(join(storage, f'{temp}.zip'), 'w')
#     for root, dirs, files in os.walk(join(storage, temp)):
#         for file in files:
#             merged.write(join(root, file), join(root.replace(join(storage, temp), ''), file))
#     merged.close()
#     # удаляем временную папку
#     # shutil.rmtree(join(storage, temp))
#     # замещаем архив текущего пользователя слитым
#     # os.rename(join(storage, f'{temp}.zip'), join(current_archive[0]))
#
#
# # разархивация с сохранением метаданных
# def unzip_with_meta(archive, destination):
#     # разархивируем архив в папку назначения
#     arch = ZipFile(archive, 'r')
#     arch.extractall(destination)
#     arch_data = {}
#     arch_root = 'home'
#     # записываем в словарь даты последнего изменения каждого файла
#     for file in arch.namelist():
#         arch_root = file[:file.find('/')]
#         arch_data[file] = time.mktime(tuple(list(arch.getinfo(file).date_time) + [0, 0, 0]))
#         # print('f', file, arch_data[file], sep='\t')
#     arch.close()
#     # возвращаем разархивированным файлам их даты изменения
#     for root, dirs, files in os.walk(join(destination, arch_root)):
#         for file in files:
#             # print(join(root, file))
#             # print(join(root, file).replace(destination, ''))
#             os.utime(
#                 join(root, file),
#                 (arch_data[join(root, file).replace(destination, '')],
#                  arch_data[join(root, file).replace(destination, '')]))

# во входе 0 - путь к архиву, 1 - путь к архивируему, то есть выбранная папка внутри архива
# разархивируем архив
def take_out(current_archive, other_archive):
    # разархивируем архив текущего пользователя во временную папку, при этом сохраним дату изменения
    current = ZipFile(current_archive[0], 'r')
    temp = str(time.time())
    unzip_with_meta(current_archive[0], join(storage, temp))
    current.close()

    # разархивируем архив другого пользрвателя в хранилище
    other = ZipFile(other_archive[0], 'r')
    unzip_with_meta(other_archive[0], storage[:-1])
    other.close()
    # сливаем полученные папки во временную, удаляем остатки другого пользователя
    for file in os.listdir(join(storage, other_archive[1])):
        if os.path.isdir(join(storage, other_archive[1], file)):
            shutil.move(join(storage, other_archive[1], file),
                        join(storage, temp, current_archive[1]))
        else:
            shutil.copy2(join(storage, other_archive[1], file),
                         join(storage, temp, current_archive[1]))
    shutil.rmtree(join(storage, other_archive[1][:other_archive[1].find('/')]))

    # создаем слитый архив и заполняем так, будто идем из корня устройства
    merged = ZipFile(join(storage, f'{temp}.zip'), 'w')
    for root, dirs, files in os.walk(join(storage, temp)):
        for file in files:
            merged.write(join(root, file), join(root.replace(join(storage, temp), ''), file))
    merged.close()
    # удаляем временную папку
    shutil.rmtree(join(storage, temp))
    # замещаем архив текущего пользователя слитым
    os.rename(join(storage, f'{temp}.zip'), join(current_archive[0]))


# разархивация с сохранением метаданных
def unzip_with_meta(archive, destination):
    # разархивируем архив в папку назначения
    arch = ZipFile(archive, 'r')
    arch.extractall(destination)
    arch_data = {}
    arch_root = 'home'
    # записываем в словарь даты последнего изменения каждого файла
    for file in arch.namelist():
        arch_root = file[:file.find('/')]
        arch_data[file] = time.mktime(tuple(list(arch.getinfo(file).date_time) + [0, 0, 0]))
    arch.close()
    # возвращаем разархивированным файлам их даты изменения
    for root, dirs, files in os.walk(join(destination, arch_root)):
        for file in files:
            os.utime(
                join(root, file),
                (arch_data[join(root, file).replace(destination + '/', '')],
                 arch_data[join(root, file).replace(destination + '/', '')])
            )


if __name__ == '__main__':
    sign_in_window()

    # take_out(('/home/peter/Study/03_semestr/Coursework/Storage/peter_Документы_v1.0.zip',
    #           '/home/peter/Документы'[1:]),
    #          ('/home/peter/Study/03_semestr/Coursework/Storage/peter_icons_v1.0.zip',
    #           '/home/peter/Study/03_semestr/Coursework/Client part/icons'[1:]))
