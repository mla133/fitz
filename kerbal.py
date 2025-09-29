from pynomo.nomographer import *
import math
isp_start=0.0
isp_stop=500.0
ve_start=0.0
ve_stop=6000.0
mr_start=1
mr_stop=9
dv_start=0
dv_stop=5000
 
def Isp(Ve):
    return Ve*9.81
    
def Prop_fraction(u):
    return 1-(1/u)
 
Ve_para={
        'tag':'A',
        'u_min':isp_start,
        'u_max':isp_stop,
        'function':lambda u:Isp(u),
        'title':r'$I_{sp}$',
        'tick_levels':5,
        'tick_text_levels':3,
        'scale_type':'linear smart',
#        'extra_params':[
#                        {
#                        'scale_type':'manual line',
#                        'tick_side':'right',
#                        'manual_axis_data':{
#                                            290:'Twitch, Mastodon',
#                                            320:"Spark, Swivel, Skipper, Cub",
#                                            340:"Rhino, Dart",
#                                            290:"Spider",
#                                            310:"Reliant, Bobcat, Mainsail",
#                                            250:"Puff",
#                                            330:"Skiff",
#                                            412:"Wolfhound",
#                                            350:"Poodle",
#                                            195:"Hammer",
#                                            165:"Flea",
#                                            220:"Kickback",
#                                            210:"Thumper",
#                                            300:'Twin-Boar',
#                                            },
#                        },
#                        {
#                        'scale_type':'manual arrow',
#                        'tick_side':'left',
#                        'arrow_length':1.5,
#                        'manual_axis_data':{
#                                            290:'Twitch, Mastodon',
#                                            315:"Ant, Vector, Mammoth",
#                                            345:"Terrier, Cheetah",
#                                            305:"Kodiak, Thud",
#                                            },
#                        }],
        'tick_side':'left',
        'title_x_shift':-0.5
        }
        
Mr_para={
        'tag':'B',
        'u_min':mr_start,
        'u_max':mr_stop,
        'function':lambda u:math.log(u),
        'title':r'$M_r$',
        'tick_levels':4,
        'tick_text_levels':3,
        'scale_type':'log smart',
        'tick_side':'right',
        'title_x_shift':0.1
        }
        
Dv_para={
        'u_min':dv_start,
        'u_max':dv_stop,
        'function':lambda u:u,
        'title':r'$\Delta{}V$',
        'tick_levels':4,
        'tick_text_levels':3,
        'scale_type':'manual line',
        'tick_side':'left',
        'title_x_shift':-0.5,
        'manual_axis_data': {
                     3400:'Kerbin Surface-Low orbit',
                     580:'Mun Surface-Low orbit',
                     1450:'Duna Surface-Low orbit',
                     390:'Ike Surface-Low orbit',
                     130:'Pol Surface-Low orbit',
                     2270:'Tylo Surface-Low orbit',
                     860:'Vall Surface-Low orbit',
                     2900:'Laythe Surface-Low orbit',
                     1690:'Kerbin-Duna Transfer',
                     4868:'Kerbin-Moho Transfer',
                     2743:'Kerbin-Eve Transfer',
                     4140:'Kerbin-Dres Transfer',
                     4000:'Kerbin-Jool Transfer',
                     3556:'Kerbin-Eeloo Transfer',
                     },
        'extra_params':[{
                        'text_format':r"$%4.0f$",
                        'u_min':dv_start,
                        'u_max':dv_stop,
                        'scale_type':'linear smart',
                        'tick_levels':4,
                        'tick_text_levels':3,
                        'tick_side':'right',
                        },
                        {
                        'scale_type':'manual point',
                        'tick_side':'right',
                        'manual_axis_data':{
                                            620:'Eeloo Surface-Low orbit',
                                            },
                        }],

        }
            
block_1_params={
             'block_type':'type_2',
             'width':20.0,
             'height':20.0,
             'f1_params':Dv_para,
             'f2_params':Mr_para,
             'f3_params':Ve_para,
             }
 
main_params={
              'filename':'Rocket_equation_nomograph.pdf',
              'paper_height':30.0,
              'paper_width':18.0,
              'block_params':[block_1_params],
              'transformations':[('scale paper',)],
              'title_str':r'Rocket Equation $\Delta{}V = V_e\ln(M_r)$'
              }
Nomographer(main_params)
