import argparse
from VulnScannerMenu import MainMenu



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--autostart", help="Autostart all Scanners", action="store_true")
    args = parser.parse_args()

    menu1 = MainMenu()
    if args.autostart:
        menu1.optionStartAll()
        print("Autostart all Scanner\n")
    menu1.show()




    # scanner1.addTarget(name="Windows-Clients", hosts="192.168.122.90,192.168.122.91,192.168.122.92,192.168.122.93", port_list_id="9ddce1ae-57e7-11e1-b13c-406186ea4fc5")

    #scanner1.listTargets()
    #scanner1.listTasks()

    # scanner1.start_task(task_id="4c33cf38-0cdd-49ee-b15a-44a30b651f4b")
    # targets = scanner1.getTargets()
    # target = scanner1.getTarget(target_id="0ddd9017-95e8-4050-869d-7b13024f71b3")
    # scanner1.addTask(target=target, scan_config="daba56c8-73ec-11df-a475-002264764cea",
    #                interval="minute", frequency="10", start_time="")
    # scanner1.addTask(target=target, scan_config="daba56c8-73ec-11df-a475-002264764cea",
    #                 interval="minute", frequency="10", start_time="")
    # print(scanner1.targets["3ee00520-c8a4-4970-b010-c30c0033560d"])

    #scanner1.start()


if __name__ == "__main__":
    main()

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="initialize scanner with data from config file")
    args = parser.parse_args()

    scanner1 = create scanner(name, cfg-file, data-file)
    scanner1.start
    scanner1.new_target
    scanner1.new_task

    print(type(gmp))

    #vulnscanner1 = VulnScanner(name="vulnscanner1")

    if args.init:
        print("init")
        #vulnscanner1.init_scanner()
    else:
        #vulnscanner1.init_scanner()
        #vulnscanner1.start_scanner()

        # vulnscanner2 = VulnScanner(name="vulnscanner2")
        # vulnscanner2.init_scanner()
        # vulnscanner2.start_scanner()

        schedule.every().minute.do(print, "minute+")

        # todo: list_targets()
        # todo: list_tasks()
        # todo: create_target(name, hosts, ex_hosts, port_list)
        # todo: create_task(target, schedule)

        # todo: add portlist to target name

        # todo: determine needed log level/priority
        # todo: delete task after x time if not finished
        # todo: delete reports from scanner after x days
        # todo: reports, tasks as object?
        # todo: delete tasks if target not available
        # todo: cli to add new hosts and new targets
            # todo: manipulate pgsql database instead of json files
            # todo: interactive tool
            # todo: 1. new target 2. list targets 3. new task 4. list tasks 5. list targets without task
            # todo: new target: name, hosts, exclude_hosts
            # todo: new task: choose target from list, define schedule
        # todo:

        while True:
            schedule.run_pending()
            time.sleep(1)

    # vulnscanner1.disconnect()


# vulnscanner1.log(0, "test")
# my_report = vulnscanner1.get_report(report_id="434bb825-c40f-4c71-9a34-f88532a2cfd0")
# my_report = vulnscanner1.get_report(report_id="434bb825-c40f-4c71-9a34-f88532a2cfd0")
# vulnscanner1.log(3, my_report)
# pretty_print(my_report)
# print(vulnscanner1.get_last_report())
# vulnscanner1.set_last_report(report_last="434bb825-c40f-4c71-9a34-f88532a2cfd1")
# vulnscanner1.get_report_count()
'''
