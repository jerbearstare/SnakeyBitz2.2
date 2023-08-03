import cairosvg
import re
import requests

#### LNbitz API INITIALATION #####
url = "https://legend.lnbits.com/withdraw/api/v1/links"
API_KEY_write = '4f185c43df804edbb0ab8cbad4973566' #write key for creating, updating and>
method_get = "get"
write_key_header = {"X-Api-Key": API_KEY_write}

score = 50

create_payload = {
    "title": "Thanks",
    "min_withdrawable": score,
    "max_withdrawable": score,
    "uses": 1,
    "wait_time": 1,
    "is_unique": "true"}
            
# API Call
create_response = requests.post(url, headers=write_key_header, json=create_payload )

# Isolate withdrawal ID
json_data = create_response.json()
withdraw_id = json_data['id']
print(withdraw_id)

svg_url = "https://legend.lnbits.com/withdraw/img/{}".format(withdraw_id)
svg_string = requests.get(svg_url).content

# svg_string = svg_string.decode('utf-8')
# filtered_svg_string = re.sub("b'|\n'", "", svg_string)
# filtered_svg_string = re.sub("\n", "<br>", filtered_svg_string)

filtered_svg_string = str(svg_string)[42:-3]

with open('QR.svg', 'w') as f:
    f.write(filtered_svg_string)

SVG_FILENAME = 'QR.svg'
PNG_FILENAME = 'QR.png'

cairosvg.svg2png(url=SVG_FILENAME, write_to=PNG_FILENAME)
 