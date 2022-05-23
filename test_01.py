import testlib
from ddt import ddt, data, unpack
import json
import copy

# change DEBUG to True to disable timeout and checks
DEBUG = True
DEBUG = False

dir_data = 'data/'

WARP = 2 # the VM
WARP = 1 # your PC

TIMEOUT = 1 * WARP  # in seconds


def get_input(input_json, key='input'):
    with open(input_json) as fr:
        js = json.load(fr)
        return js[key]


def save_images_from_tests(file_json):
    bg = '<style type="text/css"> body { background-color: #faffc7; } </style>'
    # ----------------- Save imges ------------------------------------- ##
    import os
    import images as imglib
    dir_name = os.path.splitext(file_json)[0]
    filename = os.path.basename(dir_name)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    file_path_write = os.path.join(dir_name+'/../../', filename+'.html')
    with open(file_path_write,  mode='tw') as fw:
        line  = f'{bg} <h1> HW8-req (test {filename})<h1><br/><br/>'
        line += '<h2>Expected images</h2><br/><br/>'
        images = get_input(file_json, key='expected')
        N_digit_img = len(str(len(images)))
        for count, img in enumerate(images, 1):
            # saving
            filename_img = 'img_'+str(count).zfill(N_digit_img)+'.png'
            path_img = os.path.join(dir_name, filename_img)
            imglib.save(img, path_img)
            # writing file
            line += (f'<block><img style="image-rendering: pixelated;" '
                     f'src="{path_img}" width=5%/> </block>')
        fw.write(line)
    return file_path_write


@ddt
class Test(testlib.TestCase):

    def do_test(self, input_json, doRecursionTest=True):
        '''Test implementation:
            - input_file:          name of the input JSON file. It contains input params and expected result
            TIMEOUT: global for all test
        '''
        parameters = get_input(input_json)
        if DEBUG:
            import program01 as program
            result = program.ex(**parameters)
        else:
            # first check for recursion
            if doRecursionTest:
                parameters1 = copy.deepcopy(parameters) # a complete copy for the recursion test
                with self.assertIsRecursive('program01') as program:
                    program.ex(**parameters1)
                del program
            with self.ignored_function('pprint.pprint'), \
                 self.forbidden_function('builtins.input'), \
                 self.forbidden_function('builtins.eval'), \
                 self.check_open( {'meminfo': 'rb' } ), \
                 self.check_imports(allowed=['program01', '_io']), \
                 self.imported('program01') as program, \
                 self.timeout(TIMEOUT), \
                 self.timer(TIMEOUT):
                result   = program.ex(**parameters)
        self.assertEqual(type(result),  list,     
                         'il risultato prodotto deve essere una lista / '
                         f' the expected result should be a list (got {type(result)} instead)')
        if result:
            self.assertEqual(type(result[0]),  tuple,     
                             'le immagini devono essere tuple / '
                             f'the image should be a tuple (got {type(result[0])} instead)')
        self.check_json_file_to_list(input_json, result)
        return 1
   
    #   input_json,  check_recursion
    @data(
            ( 'images_data_01.json', False),
            ( 'images_data_02.json', True ),
            ( 'images_data_03.json', True ),
            ( 'images_data_04.json', True ),
            ( 'images_data_05.json', True ),
            ( 'images_data_06.json', True ),
            ( 'images_data_07.json', True ),
            ( 'images_data_08.json', True ),
            ( 'images_data_09.json', True ),
            ( 'images_data_10.json', True ),
            ( 'images_data_11.json', True ),
            ( 'images_data_12.json', True ),
            ( 'images_data_13.json', False),
            ( 'images_data_14.json', True ),
            ( 'images_data_15.json', True ),
            ( 'images_data_16.json', True ),
            ( 'images_data_17.json', True ),
            ( 'extra_2_colors_3_D_none.json', True),
            ( 'extra_4_colors_4_D_diff.json', True),
            ( 'extra_6_colors_2_D_hrect.json', True),
            ( 'extra_4_colors_4_D_vrect.json', True),
            ( 'extra_10_colors_2_D_cross.json', True),
            ( 'extra_2_colors_3_D_none.json', True),
            ( 'extra_4_colors_2_D_diff.json', True),
            ( 'extra_2_colors_3_D_hrect.json', True),
            ( 'extra_5_colors_3_D_vrect.json', True),
            ( 'extra_6_colors_10_D_cross.json', True),
            ( 'extra_2_colors_3_D_none.json', True),
            ( 'extra_4_colors_7_D_diff.json', True),
            ( 'extra_5_colors_4_D_hrect.json', True),
            ( 'extra_3_colors_3_D_vrect.json', True),
            ( 'extra_10_colors_4_D_cross.json', True),
            ( 'extra_2_colors_3_D_none.json', True),
            ( 'extra_4_colors_2_D_diff.json', True),
            ( 'extra_2_colors_4_D_hrect.json', True),
            ( 'extra_3_colors_2_D_vrect.json', True),
            ( 'extra_2_colors_7_D_cross.json', True),
    )
    @unpack
    def test_data(self, filep, check_rec):
        return self.do_test(dir_data+filep, doRecursionTest=check_rec)


if __name__ == '__main__':
    import sys
    if len(sys.argv) == 1:
        Test.main()
    else:
        test_name = sys.argv[1] 
        print(f'> Being asked to save images for test {test_name}; saving, hold on...')
        file_path = save_images_from_tests(test_name)
        print(f'> Done! You can open the HTML page at {file_path}')
