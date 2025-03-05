import sqlite3
from sqlite3 import Error

import VulnReport
import VulnTask
import VulnTarget


class VulnScannerDB:
    __sql_create_report_table = """ CREATE TABLE IF NOT EXISTS reports (
                                id text PRIMARY KEY,
                                task_id text,
                                status text,
                                start_time text,
                                end_time text); """

    __sql_create_target_table = """ CREATE TABLE IF NOT EXISTS targets (
                                id text PRIMARY KEY,
                                name text,
                                hosts text,
                                exclude_hosts text,
                                port_list_id text); """

    __sql_create_task_table__ = """ CREATE TABLE IF NOT EXISTS tasks (
                                id text PRIMARY KEY,
                                name text,
                                target_id text,
                                scan_config_id text,
                                frequency text,
                                interval text,
                                start_time text); """

    __sql_select_report = """ SELECT * FROM reports WHERE
                                id=? """

    __sql_insert_report = """ INSERT OR REPLACE INTO reports (
                                id, task_id, status, start_time, end_time)
                                VALUES(?,?,?,?,?) """

    __sql_del_report = """ DELETE FROM reports WHERE 
                                id=? """

    __sql_select_target = """ SELECT * FROM targets WHERE
                                    id=? """

    __sql_select_all_targets = """ SELECT * FROM targets """

    __sql_insert_target = """ INSERT OR REPLACE INTO targets (
                                    id, name, hosts, exclude_hosts, port_list_id)
                                    VALUES(?,?,?,?,?) """

    __sql_del_target = """ DELETE FROM targets WHERE 
                                id=? """

    __sql_select_task = """ SELECT * FROM tasks WHERE
                                id=? """

    __sql_select_all_tasks = """ SELECT * FROM tasks """

    __sql_insert_task = """ INSERT OR REPLACE INTO tasks (
                                    id, name, target_id, scan_config_id, frequency, interval, start_time)
                                    VALUES(?,?,?,?,?,?,?) """

    __sql_del_task = """ DELETE FROM tasks WHERE
                                id=? """

    __sql_init_queue = """ SELECT * FROM reports WHERE 
                                status != 'Logged' """

    __sql_maintenance_select = """ SELECT * FROM reports 
                                WHERE task_id=? AND status=='Logged'
                                ORDER BY end_time ASC LIMIT ? """

    def __init__(self, dbFile):
        self.dbFile = dbFile
        conn = self._createConnection()
        self._createTable(conn=conn, create_table_sql=self.__sql_create_report_table)
        self._createTable(conn=conn, create_table_sql=self.__sql_create_target_table)
        self._createTable(conn=conn, create_table_sql=self.__sql_create_task_table__)
        self._closeConnection(conn=conn)

    def _runToDb(self, conn, sql_statement, values):
        try:
            c = conn.cursor()
            return c.execute(sql_statement, values)
        except Error as e:
            print(str(e))

    def _execQuery(self, sql_statement, values):
        conn = self._createConnection()
        result = self._runToDb(conn=conn, sql_statement=sql_statement, values=values)
        self._closeConnection(conn=conn)
        return result

    def _createConnection(self):
        conn = None
        dbFile = self.dbFile
        try:
            conn = sqlite3.connect(dbFile)
        except Error as e:
            print(str(e))
        return conn

    def _closeConnection(self, conn):
        conn.commit()
        #conn.close()

    def _createTable(self, conn, create_table_sql):
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(str(e))

    def selectReport(self, report: VulnReport):
        reportId = report.getId()
        report_values = (reportId,)
        return self._execQuery(sql_statement=self.__sql_select_report, values=report_values)

    def insertReport(self, report: VulnReport):
        report_values = (
        report.getId(), report.getTaskId(), report.getStatus(), report.getStartTime(), report.getEndTime())
        self._execQuery(sql_statement=self.__sql_insert_report, values=report_values)

    def deleteReport(self, report: VulnReport):
        reportId = report.getId()
        report_values = (reportId,)
        self._execQuery(sql_statement=self.__sql_del_report, values=report_values)

    def selectTarget(self, target: VulnTarget):
        targetId = target.getId()
        target_values = (targetId,)
        return self._execQuery(sql_statement=self.__sql_select_target, values=target_values)

    def getAllTargets(self):
        return self._execQuery(sql_statement=self.__sql_select_all_targets, values="")

    def insertTarget(self, target: VulnTarget):
        # todo: check if target with same hosts, excludehosts and portlist id is already in db
        target_values = (target.getId(), target.getName(), target.getHosts(), target.getExcludeHosts(), target.getPortListId())
        self._execQuery(sql_statement=self.__sql_insert_target, values=target_values)

    def deleteTarget(self, target: VulnTarget):
        targetId = target.getId()
        target_values = (targetId,)
        self._execQuery(sql_statement=self.__sql_del_target, values=target_values)

    def selectTask(self, task: VulnTask):
        taskId = task.getId()
        task_values = (taskId,)
        return self._execQuery(sql_statement=self.__sql_select_task, values=task_values)

    def getAllTasks(self):
        return self._execQuery(sql_statement=self.__sql_select_all_tasks, values="")

    def insertTask(self, task: VulnTask):
        task_values = (task.getId(), task.getName(), task.getTarget().getId(), task.getScanConfigId(), task.getFrequency(), task.getInterval(), task.getStartTime())
        self._execQuery(sql_statement=self.__sql_insert_task, values=task_values)

    def deleteTask(self, task: VulnTask):
        taskId = task.getId()
        task_values = (taskId,)
        self._execQuery(sql_statement=self.__sql_del_task, values=task_values)

    def maintenance(self, task: VulnTask, keepReports):
        task_id = task.getId()
        cur = self._execQuery(sql_statement=self.__sql_maintenance_select, values=(task_id, 100000000000000))
        rows = cur.fetchall()
        del_count = len(rows) - int(keepReports)
        if del_count > 0:
            # print(del_count)
            cur2 = self._execQuery(sql_statement=self.__sql_maintenance_select, values=(task_id, del_count))
            rows2delete = cur2.fetchall()
            # print(rows)
        else:
            rows2delete = []
        return rows2delete

    def initQueue(self):
        cur = self._execQuery(sql_statement=self.__sql_init_queue, values="")
        rows = cur.fetchall()
        return rows

    def clearQueue(self):
        cur = self._execQuery(sql_statement="DELETE FROM Reports", values="")
        rows = cur.fetchall()
        return rows
