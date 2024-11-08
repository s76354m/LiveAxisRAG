from datetime import datetime, timedelta
from typing import Callable
from apscheduler.schedulers.background import BackgroundScheduler

class TimerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.active_timers = {}
        
    def start_timer(self, timer_id: str, duration: int, callback: Callable):
        """Maps to PowerApps Timer.Start()"""
        job = self.scheduler.add_job(
            callback,
            'date', 
            run_date=datetime.now() + timedelta(milliseconds=duration),
            id=timer_id
        )
        self.active_timers[timer_id] = job 