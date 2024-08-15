from loader import parse_obj, save_obj

if __name__ == "__main__":
    input_obj = "../lesson1/6-cube.obj"
    output_obj = "./output/cube.obj"

    data = parse_obj(input_obj)

    print(data['normals'])

    save_obj(output_obj, data)