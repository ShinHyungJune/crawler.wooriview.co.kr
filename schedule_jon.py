import schedule
import time
from datetime import datetime
import kbcar_carinforamtion
import encar_carinformation

def schedule_start():
    print("────────────────────────────")
    print("Server Working Start────────")
    encar_carinformation.start_encar()
    # kbcar_carinforamtion.start_kbchacha()

# kbcar_carinforamtion.start_kbchacha()
encar_carinformation.start_encar()

schedule.every(30).minutes.do(schedule_start)

# schedule.every(1).hours.do(schedule_start)

while True:
    schedule.run_pending()

    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    print("--server active : {}".format(current_time))
    time.sleep(1)