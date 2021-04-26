from features import get_features_for_url
import pickle
import numpy as np
import sys


NON_PHISHING_URLS = [
    "http://google.com",
    "https://towardsdatascience.com/phishing-domain-detection-with-ml-5be9c99293e5",
    "https://github.com/ebubekirbbr/pdd/tree/master/input",
    "https://medium.com/intel-software-innovators/detecting-phishing-websites-using-machine-learning-de723bf2f946",
    "https://youtube.com",
    "https://www.youtube.com/watch?v=io5I7viVygM",
    "https://www.amazon.com/gp/bestsellers/?ref_=nav_em_cs_bestsellers_0_1_1_2",
    "https://zoom.us",
    "https://explore.zoom.us/meetings",
    "https://twitter.com",
    "https://twitter.com/home",
    "https://twitter.com/umasudhir/status/1384496569399975947",
]

PHISHING_URLS = [
    "https://ourdreamcars.com/BABS/BOOST/Rich/1drvme/",
    "https://century21dreamhome.info",
    "http://visaenlink.com.gt/Abono_Prestamo_FHA___Q/PVL19710001/9eeffe4b7b",
    "https://www.marsiconstructions.com/app/ingdirect_/install/index.php",
    "https://ebay.co-uk-itmad68e39b71780a69d5676b36fffe.com/56ba/john-deere",
    "https://carmovers.jplms.com.au/cenf.bsi/snnb.php",
]


def test_model(model_path):
    with open(model_path, "rb") as f:
        clf = pickle.load(f)
    if not clf:
        print("Couldn't load model!")
        return

    correct_count = 0
    incorrect_count = 0

    print("Non phishing urls - " + "*" * 30)
    for u in NON_PHISHING_URLS:
        res = get_model_res(clf, u)
        print(f"{res} : {u} (expected 0)")
        if res == 0:
            correct_count += 1
        else:
            incorrect_count += 1

    print("\nPhishing urls - " + "*" * 30)
    for u in PHISHING_URLS:
        res = get_model_res(clf, u)
        print(f"{res} : {u} (expected 1)")
        if res == 1:
            correct_count += 1
        else:
            incorrect_count += 1

    print(f"Correct Count {correct_count}")
    print(f"Incorrect Count {incorrect_count}")


def get_model_res(clf, url):
    features = get_features_for_url(url)
    feature_input = np.array(features).reshape(1, -1)
    res = clf.predict(feature_input)
    return res[0]


if __name__ == "__main__":
    model_path = None
    if len(sys.argv) > 1:
        model_path = sys.argv[1]

    model_paths = []
    if model_path is not None:
        model_paths.append(model_path)
    else:
        model_paths = [
            "./models/grega/ensemble-knn-rf-dt.pkl",
            "./models/grega/knn-model.pkl",
            "./models/grega/model.pkl",
            "./models/grega/random-forest-model-100-est.pkl",
            "./models/grega/random-forest-model.pkl",
            "./models/grega/svm.pkl",
        ]

    for p in model_paths:
        print("#" * 10)
        print(f"\nTesting for model - {p}")
        test_model(p)
