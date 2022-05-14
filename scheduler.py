from apscheduler.schedulers.blocking import BlockingScheduler
import sys, os, subprocess


if os.environ.get('REPORT_ID') is None:
    print("请配置环境变量REPORT_ID REPORT_PASSWORD", flush=True)
    sys.exit(1)
id = os.environ.get('REPORT_ID')
passwd = os.environ.get("REPORT_PASSWORD")


def exec():
    p = subprocess.Popen(['python', './main.py', id, passwd])
    # p = subprocess.Popen(['./main', id, passwd])
    p.wait()
    if p.returncode != 0:
        print("[WARNING] exited with return code " + str(p.returncode))
        return False
    return True


# exec()
def job():
    for i in range(3):
        print("USER_ID=" + id + " Attempting for the " + str(i+1) + "th time")
        print("**********************************stdout**********************************")
        if exec():
            print("Success")
            print("**********************************stdout**********************************")
            return 
        print("**********************************stdout**********************************")


scheduler_report = BlockingScheduler()
scheduler_report.add_job(job, 'cron', day='*', hour="8", minute="15", args=[], misfire_grace_time=300)
scheduler_report.add_job(job, 'cron', day='*', hour="8", minute="50", args=[], misfire_grace_time=300)
scheduler_report.add_job(job, 'cron', day='*', hour="9", minute="15", args=[], misfire_grace_time=300)
print("job started", flush=True)
scheduler_report.start()
