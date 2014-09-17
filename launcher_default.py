# coding=utf-8
import os
import sqlite3
import urllib


def pullDataBase():
    cmd = []
    cmd.append('rm -r /tmp/loadlauncher-db/ >/dev/null 2>&1')
    cmd.append('mkdir /tmp/loadlauncher-db/ >/dev/null 2>&1')
    cmd.append('adb pull /data/data/com.android.launcher/databases /tmp/loadlauncher-db/ >/dev/null 2>&1')
    os.system(';'.join(cmd))


def clearDataBase():
    cmd = 'rm -r /tmp/loadlauncher-db/ >/dev/null 2>&1'
    os.system(cmd)


def readDB():
    conn = sqlite3.connect('/tmp/loadlauncher-db/launcher.db')
    cursor = conn.cursor()
    sql = 'select intent,container,screen,cellX,cellY from favorites order by container desc,screen,cellY,cellX'
    cursor.execute(sql)
    data = cursor.fetchall()
    favorites = []
    for i in data:
        packageName, className = packageParse(i[0])
        container = i[1]
        screen = i[2]
        cellX = i[3]
        cellY = i[4]
        if packageName:
            favorites.append(makeFavoriteElement(packageName, className, container, screen, cellX, cellY))

    return '\n\n'.join(favorites)


def makeFavoriteElement(packageName, className, container, screen, cellX, cellY):
    lines = []
    lines.append('<favorite')
    lines.append('  launcher:packageName="%s"' % packageName)
    lines.append('  launcher:className="%s"' % className)
    lines.append('  launcher:container="%s"' % container)
    lines.append('  launcher:screen="%s"' % screen)
    lines.append('  launcher:x="%s"' % cellX)
    lines.append('  launcher:y="%s"' % cellY)
    lines.append('/>')
    return '\n'.join(lines)


def packageParse(intent):
    component = None
    packageName = None
    className = None
    if intent:
        item = intent.split(';')
        for i in item:
            kv = i.split('=')
            if len(kv) == 2:
                if kv[0] == 'component':
                    component = kv[1]
                    break
        if component:
            pc = component.split('/')
            packageName = urllib.unquote(pc[0])
            className = urllib.unquote(pc[1])
            if className.startswith('.'):
                className = packageName + className

    return packageName, className


if __name__ == '__main__':
    pullDataBase()
    favorites = readDB()
    print favorites
    file = open('out.txt', 'w')
    file.write(favorites)
    file.close()
    clearDataBase()




