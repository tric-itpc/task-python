from typing import List
import datetime as dt

from src.schemas.service_status import ServiceStatusOutSchema

class ServiceStats:
    def __init__(self, start_time: dt.datetime, end_time: dt.datetime, data: List[ServiceStatusOutSchema]):
        self.start_time = dt.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
        self.end_time = dt.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
        self.data = data[::-1]

    def not_online_time_total(self):
        online_time_total = 0
        prev_status = 'offline'
        prev_time = self.start_time
        first_element_created_at = self.data[0].created_at               
        current_time = self.start_time

        if first_element_created_at > self.start_time:
          self.start_time = first_element_created_at
          if self.start_time > self.end_time:
             raise ValueError

        for change in self.data:
          if change.created_at < self.start_time:
             prev_status = change.service_status
             continue
          if self.end_time < change.created_at and prev_status == 'online':
             online_time_total += (self.end_time - self.start_time).total_seconds()
             break
          if change.service_status == 'online':
            current_time = change.created_at
            if prev_status == 'offline' or prev_status == 'unstable':
                prev_time = max(prev_time, current_time)
            if current_time > self.end_time:
                current_time = self.end_time
            online_time_total += (current_time - prev_time).total_seconds()
            prev_time = current_time
            prev_status = 'online'
          elif prev_status == 'online': 
             online_time_total += (change.created_at - current_time).total_seconds()
             prev_status = change.service_status
          else:
             prev_status = change.service_status
        if prev_time < self.end_time and self.data[-1].created_at == 'online':
           online_time_total += (self.end_time - prev_time).total_seconds()
        
        online_time_total = dt.timedelta(seconds=online_time_total).total_seconds()
        total_time = (self.end_time - self.start_time).total_seconds()
        not_online_time_total = float(total_time - online_time_total)
        return total_time, online_time_total, not_online_time_total
    
    def count_sla(self):
      input_data = self.not_online_time_total()
      sla = input_data[1] / input_data[0]
      return sla