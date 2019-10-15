from Light import Service
import schedule

class WaterService(Service):
    def water(self):
        schedule.every().day.at("07:00").do(self.run_threaded_job, self.give_1_liter_water)

    def water_smart(self):
        schedule.every().day.at("08:00").do(self.run_threaded_job, self.give_water_smart)

s = WaterService()
s.start_schedule_jobs(s.water, s.water_smart())

