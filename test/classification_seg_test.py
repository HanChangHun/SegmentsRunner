import time
from pycoral.utils.dataset import read_label_file
from segments_runner.segments_runner import SegmentsRunner


def main():
    image_path = "test_data/parrot.jpg"
    segment_paths = [
        "test_data/model/mobilenet_v2_1.0_224_inat_bird_quant_segment_0_of_3_edgetpu.tflite",
        "test_data/model/mobilenet_v2_1.0_224_inat_bird_quant_segment_1_of_3_edgetpu.tflite",
        "test_data/model/mobilenet_v2_1.0_224_inat_bird_quant_segment_2_of_3_edgetpu.tflite",
    ]
    runner = SegmentsRunner(segment_paths, device="pci:0")

    labels = read_label_file("test_data/inat_bird_labels.txt")

    runner.initialize()
    runner.set_input(image_path)

    # Run inference
    print("----INFERENCE TIME----")
    for _ in range(10):
        start = time.perf_counter()
        runner.invoke_all()
        inference_time = time.perf_counter() - start
        classes = runner.get_classes()
        print("%.1fms" % (inference_time * 1000))

    print("-------RESULTS--------")
    for c in classes:
        print("%s: %.5f" % (labels.get(c.id, c.id), c.score))


if __name__ == "__main__":
    main()
