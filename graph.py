from bokeh.plotting import ColumnDataSource, figure, output_file, show
from bokeh.tile_providers import CARTODBPOSITRON, OSM, ESRI_IMAGERY, get_provider
from bokeh.transform import factor_cmap, factor_mark
from bokeh.embed import components
from bokeh.models import CheckboxGroup, CustomJS
from bokeh.layouts import row, column, gridplot
import numpy as np
import csv

def wgs84_to_web_mercator(lon, lat):

    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    
    return x, y

def lon_to_web_mercator(lon):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    return x

def lat_to_web_mercator(lat):
    k = 6378137
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return y


def readcsv(name):
    result = []
    with open(name, newline='') as csvfile:
        csvdata = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in csvdata:
            result.append(row)
    return result


def render_map():
    locations = readcsv("inputs/location_scada.csv")
    y = []
    x = []
    channel = []
    name = []
    coord = []

    for location in locations:
        coord.append(str(round(float(location[2]),4)) + ", " + str(round(float(location[3]),4)))
        y.append(lat_to_web_mercator(float(location[2])))
        x.append(lon_to_web_mercator(float(location[3])))
        if 'Radio.Modbus' in location[0]:
            channel.append('Radio Modbus')
        elif 'Radio.DNP3' in location[0]:
            channel.append('Radio DNP3')
        elif 'GPRS.DNP3' in location[0]:
            channel.append('GPRS DNP3')
        elif 'GPRS.Modbus' in location[0]:
            channel.append('GPRS Modbus')
        elif 'LAN' in location[0]:
            channel.append('LAN')
        elif 'Repetidora' in location[0]:
            channel.append('Repetidora') 
        elif 'Servidor' in location[0]:
            channel.append('Servidor') 
        elif 'New' in location[0]:
            channel.append('New') 
        else:
            channel.append('Other')
        point_positions = []
        position = 0
        while position != -1:
            position = location[0].find(".",position)
            if position != -1:
                point_positions.append(position)
                position += 1
        
        name.append(location[0][point_positions[-1]+1:])

    #output_file("map_scada.html")
    tile_provider = get_provider(OSM)

    type_channel = ['Radio DNP3','Radio Modbus','GPRS DNP3','GPRS Modbus','LAN','Repetidora','Servidor','New']
    marker_channel = ['triangle','triangle_dot','circle','circle_dot','square','star','plus','x']

    data = ColumnDataSource(data=dict(
        x=x,
        y=y,
        channel=channel,
        name=name,
        coord=coord
    ))

    TOOLTIPS = [
        ("Nombre", "@name"),
        ("Canal", "@channel"),
        ("Coordenadas","@coord")
    ]

    x_axis_start, y_axis_start =  wgs84_to_web_mercator(-80.1,-2.3)
    SIZE = 35000
    x_axis_end = x_axis_start + SIZE
    y_axis_end = y_axis_start + SIZE
    
    map = figure(x_range=(x_axis_start, x_axis_end), y_range=(y_axis_start, y_axis_end), x_axis_type="mercator", y_axis_type="mercator",tooltips

=TOOLTIPS,width=1200,height=600)
    
    
    map.add_tile(tile_provider)
    
    #for i in range(len(channel)):
    #    if channel[i] == 'Radio DNP3':
    #        map.circle(x[i],y[i],size=10,fill_alpha=0.5,fill_color='blue', source=ColumnDataSource(data=dict(name=name[i],channel=channel[i])))
    #    if channel[i] == 'GPRS DNP3':
    #        map.square(x[i],y[i],size=10,fill_alpha=0.5,fill_color='red',  source=ColumnDataSource(data=dict(name=name[i],channel=channel[i])))

    l0 = map.scatter(source=data, legend_field="channel", fill_alpha=0.6, size=20,
          marker=factor_mark('channel', marker_channel, type_channel))
          #color=factor_cmap('species', 'Category10_3', SPECIES))
    
    l1 = map.line([x[128], x[125]],[y[128],y[125]], line_width=2, line_color='black', name='Enlace Casa Quimica - Las Cabras')

    checkbox = CheckboxGroup(labels=["Outstations", "Links"],active=[0, 1],width=100)
    checkbox.js_on_click(CustomJS(code="""xline.visible = false; // same xline passed in from args
                            yline.visible = false;
                            // cb_obj injected in by the callback
                            if (cb_obj.active.includes(0)){xline.visible = true;} // 0 index box is xline
                            if (cb_obj.active.includes(1)){yline.visible = true;}""",
                    args={'xline': l0, 'yline': l1}
    ))

    #map.sizing_mode = "stretch_both" 
    layout = column(checkbox, map)

    script, div = components(layout)

    return script, div

    #show(map)

    #map.circle('x','y',radius=100,fill_alpha=0.5,fill_color='blue', source = data)

    #TOOLTIPS = [('Organisation', '@OrganisationName')]
    #p = figure(background_fill_color="lightgrey", tooltips=TOOLTIPS)

if __name__=="__main__":
    pass