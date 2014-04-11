#!/usr/bin/env python
# coding=utf-8
import os
import re
import datetime
import sys
import threading
import urllib
import urllib2
import uuid
import thread
import time

release_dir = 'release_img'
target_produce_path = 'out/target/product/baoxue/'
web_server_path = '/mnt/web'
#web_server_path = 'web'
ProjectConfigPath = 'mediatek/config/baoxue/ProjectConfig.mk'
modem_base_path = 'mediatek/custom/common/modem/'
APDB_path = 'mediatek/cgen/APDB_MT6572_S01_ALPS.JB3.MP_'
fat_sparse_file = 'fat_sparse.img'
default_fat_sparse_path = 'prebuilts/android-arm/sdcard/' + fat_sparse_file
scatter_file = 'MT6572_Android_scatter.txt'
copy_files = [scatter_file,
              'preloader_baoxue.bin',
              'MBR',
              'EBR1',
              'lk.bin',
              'boot.img',
              'recovery.img',
              'secro.img',
              'logo.bin',
              'cache.img']

copy_dirs = ['system',
             'data']

ex_config_file_name = 'changeBinEX_config'

writeLock = threading.RLock()
thread_count = 0


def addThreadCount():
    global writeLock, thread_count
    writeLock.acquire()
    thread_count = thread_count + 1
    writeLock.release()


def subThreadCount():
    global writeLock, thread_count
    writeLock.acquire()
    thread_count = thread_count - 1
    writeLock.release()


def getShell(cmd):
    return os.popen(cmd).readlines()


def delDir(dir):
    os.system('rm -r %s >/dev/null 2>&1' % dir)


def copyDir(src, des):
    os.system('cp -a %s %s' % (src, des))


def copyFile(src, des):
    os.system('cp -p %s %s' % (src, des))


def copyFileNoTime(src, des):
    os.system('cp %s %s' % (src, des))


def mv(src, des):
    os.system('mv %s %s' % (src, des))


def getProp(file, key):
    file = open(file)
    value = None
    for i in file.readlines():
        kv = i.split('=')
        if len(kv) == 2 and kv[0].strip() == key:
            value = kv[1].strip()
            break
    file.close()
    return value


def setProp(file_path, key, value):
    file = open(file_path)
    lines = file.readlines()
    new_lines = []
    file.close()
    for i in lines:
        kv = i.split('=')
        if len(kv) == 2 and kv[0].strip() == key:
            i = '%s=%s' % (key, value)
        new_lines.append(i.strip())
    file = open(file_path, 'w')
    file.write('\n'.join(new_lines))
    file.close()


def getBPLPath(base_path, modem_name):
    modem_path = os.path.join(base_path, modem_name)
    for i in os.listdir(modem_path):
        if i.startswith('BPL'):
            return os.path.join(modem_path, i)


def subExists(sub):
    path = 'changeBin_' + sub
    return os.path.exists(path)


def getExConfig(sub):
    out = []
    out_all = []
    out_sub = []

    path_all = ex_config_file_name
    if os.path.exists(path_all):
        file = open(path_all)
        for i in file.readlines():
            if i.strip():
                out_all.append(i.strip())
        file.close()

    path_sub = os.path.join('changeBin_' + sub, ex_config_file_name)
    if os.path.exists(path_sub):
        file = open(path_sub)
        for i in file.readlines():
            if i.strip():
                out_sub.append(i.strip())
        file.close()
    if len(out_all) > 0:
        for i in out_all:
            if len(out_sub) > 0:
                for j in out_sub:
                    out.append(i + "@" + j)
            else:
                out.append(i)
    else:
        for j in out_sub:
            out.append(j)

    if len(out) > 0:
        print(out)
        return out
    else:
        return None


def do_sys_argv():
    global subs, nocopy, source_path, change_mode, source_base_path
    subs = []
    tem_subs = []
    nocopy = False
    find_all = False
    state = 0
    source_base_path = None
    source_path = target_produce_path
    change_mode = False
    source_zip = None

    for i in range(1, len(sys.argv)):
        a = str(sys.argv[i])
        if state == 0:
            if a.startswith('-'):
                if a == '-n':
                    nocopy = True
                elif a == '-a':
                    find_all = True
                elif a == '-s':
                    change_mode = True
                    state = 1

            elif not find_all:
                tem_subs.append(a)
        elif state == 1:
            source_zip = a
            state = 0
    if find_all:
        subs = []
        for i in os.listdir('.'):
            if i.startswith('changeBin_'):

                sub = i.replace('changeBin_', '')
                ex_config = getExConfig(sub)
                if not ex_config:
                    subs.append(sub)
                else:
                    for j in ex_config:
                        subs.append(sub + '@' + j)
    else:
        for i in tem_subs:
            if subExists(i):
                ex_config = getExConfig(i)
                if not ex_config:
                    subs.append(i)
                else:
                    for j in ex_config:
                        subs.append(i + '@' + j)
            else:
                sys.stderr.write('not exists:%s\n' % i)
    if change_mode:
        source_base_path = 'unzip_src_' + str(uuid.uuid1())
        os.mkdir(source_base_path)
        os.system('./unbuild %s %s' % (source_zip, source_base_path))
        source_path = os.path.join(source_base_path, release_dir)


def split_version(custom_version):
    if custom_version.startswith('eng.'):
        type = 'eng'
    else:
        type = 'user'
    custom_version = custom_version.replace('eng.', '').replace('user.', '')
    re1 = re.compile(r'^([^-_]+)_([^-_]+)_([^-_]+)_([^-_]+)$')
    match = re1.match(custom_version)
    if match:
        groups = match.groups()
        project = groups[0]
        custom = groups[1]
        branch = groups[2]
        version = groups[3]
        subversion = None
    else:
        re2 = re.compile(r'^([^-_]+)_([^-_]+)_([^-_]+)-([^-_]+)_([^-_]+)$')
        match = re2.match(custom_version)

        groups = match.groups()
        project = groups[0]
        custom = groups[1]
        branch = groups[2]
        subversion = groups[3]
        version = groups[4]

    return {'type': type,
            'project': project,
            'custom': custom,
            'branch': branch,
            'subversion': subversion,
            'version': version,

    }


def format_version(type, version, timestamp=None, subversion=None):
    if type == 'tpcbv_t':
        return "%s_%s_%s_%s_%s_%s" % (version['type'],
                                      version['project'],
                                      version['custom'],
                                      version['branch'],
                                      version['version'],
                                      timestamp)
    elif type == 'tpcbsv_t':
        return "%s_%s_%s_%s-%s_%s_%s" % (version['type'],
                                         version['project'],
                                         version['custom'],
                                         version['branch'],
                                         subversion,
                                         version['version'],
                                         timestamp)
    elif type == 'tpcbsv':
        return "%s_%s_%s_%s-%s_%s" % (version['type'],
                                      version['project'],
                                      version['custom'],
                                      version['branch'],
                                      subversion,
                                      version['version'])
    elif type == 't.pcbsv':
        return "%s.%s_%s_%s-%s_%s" % (version['type'],
                                      version['project'],
                                      version['custom'],
                                      version['branch'],
                                      subversion,
                                      version['version'])
    elif type == 'pcbv':
        return "%s_%s_%s_%s" % (version['project'],
                                version['custom'],
                                version['branch'],
                                version['version'])
    elif type == 'pcb':
        return "%s_%s_%s" % (version['project'],
                             version['custom'],
                             version['branch'])


def scatter_fat_img(path):
    scatter_path = os.path.join(path, scatter_file)
    fat_sparse_path = os.path.join(path, fat_sparse_file)
    if os.path.exists(fat_sparse_path):
        out = ''
        partition_name = ''
        f = open(scatter_path, 'r')
        line = f.readline()
        while line:
            line = line.strip('\n')
            parms = line.split(':')
            if len(parms) == 2:
                key = parms[0].strip(' ')
                value = parms[1].strip(' ')
                if key == 'partition_name':
                    partition_name = value
                if partition_name == 'FAT':
                    if key == 'file_name':
                        line = '  file_name: fat_sparse.img'
                    elif key == 'is_download':
                        line = '  is_download: true'
                    elif key == 'type':
                        line = '  type: fat'
            out += line + '\n'
            line = f.readline()
        f.close()
        f = open(scatter_path, 'w')
        f.write(out)
        f.close()


def test_exists(test_path):
    res = True
    for i in copy_files:
        path = os.path.join(test_path, i)
        if not os.path.exists(path):
            sys.stderr.write('***Not found %s\n' % path)
            res = False

    for i in copy_dirs:
        path = os.path.join(test_path, i)
        if not os.path.exists(path):
            sys.stderr.write('***Not found %s\n' % path)
            res = False
    return res


def package(tmp_dir, version, timestamp, subversion, ):
    global nocopy
    if not nocopy:
        version_formated = format_version('tpcbsv_t', version, timestamp, subversion)
    else:
        version_formated = format_version('tpcbsv', version, subversion=subversion)

    zipname = version_formated + '.zip'
    cmds = []

    delDir(zipname)
    cmds.append('cd ' + tmp_dir)
    cmds.append('zip -r -1 ../%s *' % zipname)
    os.system(';'.join(cmds))
    delDir(tmp_dir)
    print ''
    print ''
    print version_formated
    print ''
    print ''
    return zipname


def postVersion(v):
    url = 'http://192.168.1.2:8000/version/log.py'
    values = {'v': v}
    data = urllib.urlencode(values)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    the_page = response.read()


def copy_to_server(zip_name, version, timestamp, subversion):
    global success_files,nocopy
    if not nocopy:
        version_formated = format_version('tpcbsv_t', version, timestamp, subversion)
    else:
        version_formated = format_version('tpcbsv', version, subversion=subversion)
    des_dir = os.path.join(web_server_path, version['custom'], version['project'],
                           format_version('pcb', version), format_version('tpcbv_t', version, timestamp=timestamp))
    if not os.path.isdir(des_dir):
        os.makedirs(des_dir)
    print ('copying ' + zip_name)
    copyFileNoTime(zip_name, des_dir)
    if os.path.exists(os.path.join(des_dir, zip_name)):
        print ('cp %s %s Success!' % (zip_name, des_dir))
        postVersion(zip_name)
        success_files.append(version_formated)


def package_and_copy_to_server(tmp_dir, version, timestamp, subversion):
    global nocopy
    try:
        zip_name = package(tmp_dir, version, timestamp, subversion)

        if not nocopy:
            copy_to_server(zip_name, version, timestamp, subversion)
    except Exception, e:
        print e
        pass
    subThreadCount()


def main():
    global subs, success_files, source_path, change_mode, source_base_path

    start_time = datetime.datetime.now()
    success_files = []
    do_sys_argv()
    shell_format_date_utc = getShell('date +%s')[0]
    shell_format_date = getShell('date')[0]
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M')
    modem_name = getProp(ProjectConfigPath, 'CUSTOM_MODEM')
    BPL_path = getBPLPath(modem_base_path, modem_name)

    if test_exists(source_path):
        for sub in subs:
            delDir(release_dir)
            if os.path.exists(release_dir):
                sys.stderr.write('del error\n')
                exit()
            os.mkdir(release_dir)
            #拷贝文件
            if not change_mode:
                for file in copy_files:
                    src = os.path.join(source_path, file)
                    print 'copying %s' % file
                    copyFile(src, release_dir)
                for file in copy_dirs:
                    src = os.path.join(source_path, file)
                    print 'copying %s' % file
                    copyDir(src, release_dir)
                copyFile(APDB_path, release_dir)
                copyFile(default_fat_sparse_path, release_dir)
            else:
                os.system('cp -a %s/* %s' % (source_path, release_dir))
            #读取build.prop属性
            build_prop_path = os.path.join(release_dir, 'system/build.prop')
            custom_version = getProp(build_prop_path, 'ro.custom.build.version')
            version = split_version(custom_version)
            #拷贝BPL文件
            if not change_mode:
                copyFile(BPL_path, os.path.join(release_dir, format_version('pcbv', version) + '.src'))
            #修改build.prop属性
            new_prop_version = format_version('t.pcbsv', version, subversion=sub)
            setProp(build_prop_path, 'ro.custom.build.version', new_prop_version)
            setProp(build_prop_path, 'ro.build.date.utc', shell_format_date_utc)
            setProp(build_prop_path, 'ro.build.date', shell_format_date)
            if sub.find('@') == -1:
                print 'execute %s' % sub
                os.system('cd %s;./build' % ('changeBin_' + sub,))
            else:
                ex_subs = sub.split('@')
                print 'execute changeBin_%s' % ex_subs[0]
                os.system('cd changeBin_%s;./build' % ex_subs[0])
                for ex in range(1, len(ex_subs)):
                    print 'execute changeBinEX_%s' % ex_subs[ex]
                    os.system('cd changeBinEX_%s;./build' % ex_subs[ex])

            print 'build system and data for %s' % sub
            os.system('./systemDataImgBuild')
            delDir(os.path.join(release_dir, 'system'))
            delDir(os.path.join(release_dir, 'data'))
            scatter_fat_img(release_dir)
            tmp_dir = 'tmp_' + str(uuid.uuid1())
            os.mkdir(tmp_dir)
            mv(release_dir, tmp_dir)
            while thread_count > 5:
                time.sleep(1)
            addThreadCount()
            thread.start_new_thread(package_and_copy_to_server, (tmp_dir, version, timestamp, sub))

        while thread_count > 0:
            time.sleep(1)
        success_files.sort()
        print ""
        print ""
        for i in success_files:
            print i
    inv = datetime.datetime.now() - start_time
    if change_mode:
        delDir(source_base_path)
    print 'elapsed time:' + str(inv)


main()
