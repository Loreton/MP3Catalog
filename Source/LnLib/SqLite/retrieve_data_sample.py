#!/usr/bin/env python3
#
# -*- coding: iso-8859-1 -*-

# http://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

# ####################################################################################################
# -
# ####################################################################################################
import sqlite3

def printDB():


    cursor.execute("""
                select id, priority, details, status, deadline from task where project = 'pymotw'
                """)

    for row in cursor.fetchall():
        task_id, priority, details, status, deadline = row
        print '%2d {%d} %-20s [%-8s] (%s)' % (task_id, priority, details, status, deadline)


    '''
    cursor.execute("""
                select id, priority, details, status, deadline from task where project = 'pymotw'
                """)

    for row in cursor.fetchall():
        task_id, priority, details, status, deadline = row
        print '%2d {%d} %-20s [%-8s] (%s)' % (task_id, priority, details, status, deadline)
    '''