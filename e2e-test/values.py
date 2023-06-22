from bs4 import BeautifulSoup

html = '''
<ul class="RX2iAqpXZsTQWN9kH7A9"><li><button data-theme="dark" value="Ilyinikh Media Productions" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">Ilyinikh Media Productions</span></button></li><li><button data-theme="dark" value="AndreyVision Films" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">AndreyVision Films</span></button></li><li><button data-theme="dark" value="Moscow Motion Pictures" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">Moscow Motion Pictures</span></button></li><li><button data-theme="dark" value="Ilyinikh Creative Studios" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">Ilyinikh Creative Studios</span></button></li><li><button data-theme="dark" value="Pixel Perfect Productions" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">Pixel Perfect Productions</span></button></li><li><button data-theme="dark" value="Moscow Motion Media" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">Moscow Motion Media</span></button></li><li><button data-theme="dark" value="Creative Camera Crew" class="MuiButton-root otNW4coqlEK2_WdUbbRs e7PbnvwTl4P0JWSxgRDP ErG0lFnNjDwJOptMcR2Q" type="button"><span class="l2">Creative Camera Crew</span></button></li></ul>'''

soup = BeautifulSoup(html, 'html.parser')
buttons = soup.find_all('button')

values = [button['value'] for button in buttons]

print(values)
