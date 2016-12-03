import csv

def read_anomaly_period(anomaly_file_name):
    csvfile = open(anomaly_file, 'r')
    reader = csv.DictReader(csvfile)
    anomalies = []
    for row in reader:
        anomaly_ts = float(row['Timestamp'])
        anomaly_duration = float(row['Duration'])
        cur_anomaly = [anomaly_ts, anomaly_ts + anomaly_duration]
        anomalies.append(cur_anomaly)

    return anomalies

def read_anomaly_ts(anomaly_file_name):
    csvfile = open(anomaly_file_name, 'r')
    reader = csv.DictReader(csvfile)
    anomaly_tses = []
    for row in reader:
        anomaly_ts = float(row['Timestamp'])
        anomaly_tses.append(anomaly_ts)

    return anomaly_tses

def read_anomaly_info(anomaly_file_name):
    csvfile = open(anomaly_file_name, 'r')
    reader = csv.DictReader(csvfile)
    anomaly_info = {}
    for row in reader:
        anomaly_ts = float(row['Timestamp'])
        anomaly_info[anomaly_ts] = {'Parameter':int(row['Parameter']), 'Type':row['Type'], 'Server':row['Server']}

    return anomaly_info

def read_bw_change_info(bw_change_file):
    csvfile = open(bw_change_file, 'r')
    reader = csv.DictReader(csvfile)
    bw_change_info = {}
    for row in reader:
        bw_change_ts = float(row['Timestamp'])
        bw_change_info[bw_change_ts] = {'orgBW':int(row['orgBW']), 'curBW':row['curBW'], 'Server':row['Server']}

    return bw_change_info

if __name__ == "__main__":
    anomaly_file = "D://GitHub/pyDraw/tcc-data/qoe-models/anomaly.csv"
    anomalies = read_anomaly_ts(anomaly_file)
    print anomalies

