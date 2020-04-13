import re
import threading
import time
import winsound

import pyperclip

frequency = 880  # Set Frequency To 2500 Hertz
duration = 200  # Set Duration To 1000 ms == 1 second

s = """
#define REGISTER_AOVS 
data->aovs.clear(); 
data->aovs.push_back(params[p_aov_diffuse_color].STR); 
data->aovs.push_back(params[p_aov_direct_diffuse].STR); 
data->aovs.push_back(params[p_aov_direct_diffuse_raw].INT); 
data->aovs.push_back(params[p_aov_indirect_diffuse].STR); 
data->aovs.push_back(params[p_aov_indirect_diffuse_raw].STR); 
data->aovs.push_back(params[p_aov_direct_backlight].STR); 
data->aovs.push_back(params[p_aov_indirect_backlight].STR); 
data->aovs.push_back(params[p_aov_direct_specular].STR); 
data->aovs.push_back(params[p_aov_indirect_specular].STR); 
data->aovs.push_back(params[p_aov_direct_specular_2].STR); 
data->aovs.push_back(params[p_aov_indirect_specular_2].STR); 
data->aovs.push_back(params[p_aov_single_scatter].STR); 
data->aovs.push_back(params[p_aov_sss].STR); 
data->aovs.push_back(params[p_aov_refraction].STR); 
data->aovs.push_back(params[p_aov_emission].STR); 
data->aovs.push_back(params[p_aov_uv].STR); 
data->aovs.push_back(params[p_aov_depth].STR); 
data->aovs.push_back(params[p_aov_light_group_1].STR); 
data->aovs.push_back(params[p_aov_light_group_2].STR); 
data->aovs.push_back(params[p_aov_light_group_3].STR); 
data->aovs.push_back(params[p_aov_light_group_4].STR); 
data->aovs.push_back(params[p_aov_light_group_5].STR); 
data->aovs.push_back(params[p_aov_light_group_6].STR); 
data->aovs.push_back(params[p_aov_light_group_7].STR); 
data->aovs.push_back(params[p_aov_light_group_8].STR); 
data->aovs.push_back(params[p_aov_light_group_9].STR); 
data->aovs.push_back(params[p_aov_light_group_10].STR); 
data->aovs.push_back(params[p_aov_light_group_11].STR); 
data->aovs.push_back(params[p_aov_light_group_12].STR); 
data->aovs.push_back(params[p_aov_light_group_13].STR); 
data->aovs.push_back(params[p_aov_light_group_14].STR); 
data->aovs.push_back(params[p_aov_light_group_15].STR); 
data->aovs.push_back(params[p_aov_light_group_16].STR); 
data->aovs.push_back(params[p_aov_id_1].STR); 
data->aovs.push_back(params[p_aov_id_2].STR); 
data->aovs.push_back(params[p_aov_id_3].STR); 
data->aovs.push_back(params[p_aov_id_4].STR); 
data->aovs.push_back(params[p_aov_id_5].STR); 
data->aovs.push_back(params[p_aov_id_6].STR); 
data->aovs.push_back(params[p_aov_id_7].STR); 
data->aovs.push_back(params[p_aov_id_8].STR); 
assert(NUM_AOVs == data->aovs.size() && "NUM_AOVs does not match size of aovs array!"); 
for (size_t i=0; i < data->aovs.size(); ++i) 
    	AiAOVRegister(data->aovs[i].c_str(), AI_TYPE_RGB, AI_AOV_BLEND_OPACITY); 
data->aovs_rgba.clear(); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_1].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_2].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_3].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_4].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_5].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_6].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_7].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_8].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_9].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_10].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_11].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_12].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_13].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_14].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_15].STR); 
data->aovs_rgba.push_back(params[p_aov_shadow_group_16].STR); 
assert(NUM_AOVs_RGBA == data->aovs_rgba.size() && "NUM_AOVs_RGBA does not match size of aovs_rgba array!"); 
for (size_t i=0; i < data->aovs_rgba.size(); ++i) 
        AiAOVRegister(data->aovs_rgba[i].c_str(), AI_TYPE_RGBA, AI_AOV_BLEND_OPACITY); 
"""

detect_string = "params["


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


apts = ['INT', 'STR', 'BOOL', 'FLT']


def get_function_for_type(type_id):
    if type_id == "INT":
        return "Int"
    if type_id == "FLT":
        return "Flt"
    if type_id == "STR":
        return "Str"
    if type_id == "BOOL":
        return "Bool"


def fix_content(content):
    print("Hello from migrate, run")
    result = ""

    i = 0
    for line in content.splitlines():
        i += 1
        # if i > 10:
        #    break

        param_index = line.find(detect_string)
        if param_index > -1:
            # print(param_index)
            # print(line[line.index(detect_string) + len(detect_string):])
            print("line", i, ": ", line)
            left_string = line[0:param_index]
            print("left_string: ", left_string)
            mid_string = line[param_index + len(detect_string):]
            print("mid_string: ", mid_string)
            string_parts = mid_string.split("].")
            print("string_parts: ", string_parts)
            parameter_name = remove_prefix(string_parts[0], "p_")

            key_type_match = re.findall(r"[\w']+", string_parts[1])
            print("re.findall: ", key_type_match)

            # splits = [string_parts[1].split(apt) for apt in apts]
            # print("splits: ", splits)
            r = re.compile(r"(\b)|(\b)".join(apts))
            splits = r.sub("", string_parts[1])
            print("splits: ", splits)
            # end_str = ");"
            end_str = splits

            # end_split = string_parts[1].split(");")
            end_split = string_parts[1].split("BOOL")
            print("end_split: ", end_split)
            # print(end_split, "=", len(end_split))

            # if len(end_split) > 1:
            #    end_str = ");" + end_split[1]
            print("end_str: ", end_str)
            function_name = "AiNodeGet" + get_function_for_type(key_type_match[0])
            result_line = "{}{}(node, \"{}\"){}".format(left_string.strip(), function_name.strip(), parameter_name,
                                                        end_str)
            # print(result_line)
            result += result_line + "\r\n"
        else:
            result += line + "\r\n"

    return result


def contains_keywords(string):
    #    if url.startswith("http://") and not "bit.ly" in url:
    #        return True
    #    detect = "bit.ly"
    #    if string.startswith("http://") and not detect in string:
    #        return True
    param_index = string.find(detect_string)
    if param_index > -1:
        return True
    return False


def content_received(clipboard_content):
    # print("Found url: %s" % str(clipboard_content))
    result = fix_content(clipboard_content)
    print(result)
    pyperclip.copy(result)
    spam = pyperclip.paste()
    winsound.Beep(frequency, duration)


class ClipboardWatcher(threading.Thread):
    def __init__(self, predicate, callback, pause=5.):
        super(ClipboardWatcher, self).__init__()
        self._predicate = predicate
        self._callback = callback
        self._pause = pause
        self._stopping = False

    def run(self):
        recent_value = ""
        while not self._stopping:
            tmp_value = pyperclip.paste()
            if tmp_value != recent_value:
                recent_value = tmp_value
                if self._predicate(recent_value):
                    self._callback(recent_value)
            time.sleep(self._pause)

    def stop(self):
        self._stopping = True


def main():
    watcher = ClipboardWatcher(contains_keywords, content_received, 1.)
    watcher.start()
    while True:
        try:
            print("Waiting for changed clipboard...")
            time.sleep(10)
        except KeyboardInterrupt:
            watcher.stop()
            break


if __name__ == "__main__":
    print("Hello from migrate, main")
    main()

# if __name__ == '__main__':
#    fix_content(s)
