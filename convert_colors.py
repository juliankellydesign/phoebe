import json
import colorsys

def rgb_to_hsl(r, g, b):
    # Convert RGB values from 0-1 to 0-255
    r, g, b = r * 255, g * 255, b * 255
    # Convert to HSL
    h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
    # Convert to degrees and percentages
    h = round(h * 360)
    s = round(s * 100)
    l = round(l * 100)
    return {"h": h, "s": s, "l": l}

def convert_colors_in_json(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Process each variable
    for variable in data['variables']:
        if variable['type'] == 'COLOR':
            # Convert the color value
            rgb_value = variable['valuesByMode']['1:0']
            if isinstance(rgb_value, dict) and 'r' in rgb_value:
                hsl_value = rgb_to_hsl(rgb_value['r'], rgb_value['g'], rgb_value['b'])
                variable['valuesByMode']['1:0'] = hsl_value
                
                # Also convert the resolved value
                resolved_value = variable['resolvedValuesByMode']['1:0']['resolvedValue']
                if isinstance(resolved_value, dict) and 'r' in resolved_value:
                    hsl_resolved = rgb_to_hsl(resolved_value['r'], resolved_value['g'], resolved_value['b'])
                    variable['resolvedValuesByMode']['1:0']['resolvedValue'] = hsl_resolved
    
    # Write the modified data back to a new file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    convert_colors_in_json('Core.json', 'Core_HSL.json') 