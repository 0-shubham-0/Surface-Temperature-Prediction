def combine_rgb(red, green, blue):
    rgb = (red << 16) | (green << 8) | blue
    return rgb

def extract_rgb(rgb):
    red = (rgb >> 16) & 0xFF
    green = (rgb >> 8) & 0xFF
    blue = rgb & 0xFF
    return red, green, blue

def create_csv(img_path, csv_path, new_width, new_height):
    from PIL import Image
    import csv

    # Load the temperature color map image
    image = Image.open(img_path)
    image = image.resize((new_width, new_height))


    # Define the temperature range and corresponding RGB values
    temperature_range = (0, 50)  # Temperature range from 0 to 50 degrees Celsius
    color_range = [(255, 0, 0), (255, 255, 0), (0, 255, 0)]  # RGB color gradient from red to yellow to green

    # Create a CSV file to store the temperature data
    csv_file = open(csv_path, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["X", "Y", "rgb"])

    # Iterate over each pixel in the image and extract temperature data
    pixels = image.load()
    width, height = image.size
    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r == 0 and g == 0 and b == 0:
                temperature = -1
            else:
                # Calculate the temperature based on the color gradient
                # progress = (r / 255)  # Calculate the progress within the gradient (0 to 1)
                # temperature = temperature_range[0] + (temperature_range[1] - temperature_range[0]) * progress
                temperature = combine_rgb(r, g, b)

            # Save the temperature data along with the pixel position to the CSV file
            csv_writer.writerow([x, y, int(temperature)])

    # Close the CSV file
    csv_file.close()

def create_img(csv_path, img_path):
    import numpy as np
    import csv
    from PIL import Image

    # Read temperature data from CSV file
    temperature_data = []

    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
            x, y, temperature = map(int, row)
            temperature_data.append((x, y, temperature))

    # Find min and max temperature values
    temperatures = [temp for _, _, temp in temperature_data]

    # find min temperaute but skip -1
    min_temp = min([temp for temp in temperatures if temp != -1])
    max_temp = max(temperatures)

    # Create an empty image array
    width = max(x for x, _, _ in temperature_data) + 1
    height = max(y for _, y, _ in temperature_data) + 1
    image_array = np.zeros((height, width, 3), dtype=np.uint8)

    # Convert temperature values back to color and fill the image array
    for x, y, temperature in temperature_data:
        if temperature == -1:
            color = (0,0,0)
        else:
            # Interpolate color based on temperature value
            # normalized_temp = (temperature - min_temp) / (max_temp - min_temp)
            # green = int(255 * (1 - normalized_temp))
            # red = int(255 * normalized_temp)
            # color = (red, green, 0)  # Set blue channel to 0
            color = extract_rgb(temperature)

        # Fill the corresponding pixel in the image array with the interpolated color
        image_array[y, x] = color

    # Create and save the image
    image = Image.fromarray(image_array)
    image.save(img_path)

    print("Image restored from temperature data and saved as temp_color_map_restored.jpg")