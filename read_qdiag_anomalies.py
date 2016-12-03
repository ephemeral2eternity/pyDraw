import json
import calendar
from datetime import datetime
import glob

# def draw_anomalies_per_type(total_anomalies):


def read_qdiag_anomalies(json_file_name, time_start, time_end):
    anomaly_dict = json.load(open(json_file_name))

    anomalies = []
    for id in anomaly_dict.keys():
        cur_ts = float(anomaly_dict[id]['timestamp'])
        if (cur_ts > time_start) and (cur_ts < time_end):
            anomalies.append(anomaly_dict[id])

    return anomalies

if __name__ == '__main__':
    anomalies_folder = 'D:\\Data\\QDiag\\20161201\\anomalies\\'
    anomaly_files = glob.glob(anomalies_folder + "*.json")

    start_time = "2016-12-02 00:00:00"
    start_time_ts = calendar.timegm(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S").timetuple())
    print start_time_ts

    end_time = "2016-12-02 02:00:00"
    end_time_ts = calendar.timegm(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S").timetuple())
    print end_time_ts

    total_anomalies = []
    for anomaly_file in anomaly_files:
        cur_anomalies = read_qdiag_anomalies(anomaly_file, start_time_ts, end_time_ts)
        total_anomalies = total_anomalies + cur_anomalies

    print "There are totally " + str(total_anomalies.__len__()) + " anomalies!"

