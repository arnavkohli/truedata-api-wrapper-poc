from truedata_ws.websocket.TD import TD
from pprint import pprint
from copy import deepcopy
import time, json, pandas, sys

USERNAME = ''
PASSWORD = ''
FILE_NAME = 'symbol_data.xlsx'



def props(cls):   
  return [i for i in cls.__dict__.keys() if i[:1] != '_']

def main(delay=None):
	td_app = TD(USERNAME, PASSWORD)

	# Import Symbols
	with open('./symbols.json', 'r') as f:
		symbols = json.loads(f.read())

	print (f'Total Symbols: {len(symbols)}')

	req_ids = td_app.start_live_data(['APOLLOHOSP20SEP920PE'])
	live_data_objs = {}
	time.sleep(2)

	while True:
		all_data = []
		for req_id in req_ids:
		    live_data_objs[req_id] = deepcopy(td_app.live_data[req_id])
		    data = td_app.touchline_data[req_id]
		    print (data)
		    all_data.append({i : data.__getattribute__(i) for i in props(data)})
		    time.sleep(0.1)


		print ('[INFO] Extracting to excel...')
		pandas.DataFrame(all_data).to_excel(FILE_NAME)

		if delay:
			time.sleep(delay)
		else:
			return

if __name__ == '__main__':
	args = sys.argv
	try:
		cmd = args[1]
		val = args[2]
	except:
		exit(f'[INVALID] Please use correct format. python {__file__} delay <delay_in_seconds>')

	if cmd != 'delay':
		exit(f'[INVALID] Please use correct format. python {__file__} delay <delay_in_seconds>')

	try:
		val = int(val)
	except:
		exit(f'[INVALID] Delay should be valid integer.')

	main(delay=val)
