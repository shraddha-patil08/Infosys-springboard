from ultralytics import YOLO
import cv2
import random

class Tracker:

    def __init__(self):
        self.model = YOLO("yolov8x.pt")

    def detect_objects(self, frames):

        detections = []

        for frame in frames:
            deteced_objs = self.detect_frame(frame)
            detections.append(deteced_objs)
        # for i in range(0, len(frames),5):
        #     frame = frames[i]
        #     detected_objs = self.detect_frame(frame)
        #     detections.append(detected_objs)

        return detections

    def detect_frame(self,frame):
        results = self.model.track(frame, persist=True)[0]
        name_dict = results.names

        valid_objects = ['bicycle','car','motorcycle','bus','truck']

        dict = {}
        for box in results.boxes:
            track_id = int(box.id.tolist()[0])
            result = box.xyxy.tolist()[0]
            object_class_id = box.cls.tolist()[0]
            object_class_name = name_dict[object_class_id]
            # if object_class_name == "car":
            #     dict[track_id] = result


            if object_class_name in valid_objects:
                dict[track_id] = {object_class_name: result}

        return dict

    def draw_annotations(self, frames, object_detections):
        output_video_frames = []

        color_dict = {
            'bicycle': (0, 255, 0),  # Green
            'car': (255, 0, 0),  # Blue
            'motorcycle': (0, 0, 255),  # Red
            'bus': (255, 255, 0),  # Cyan
            'truck': (0, 255, 255),  # Yellow
        }


        for frame, obj_detected in zip(frames, object_detections):
            for track_id, obj_details in obj_detected.items():
                for object_class, bbox in obj_details.items():
                    x1,y1,x2,y2 = bbox
                    object_color = color_dict.get(object_class, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))

                    # Put text on the bbox
                    label = f"{object_class} {track_id}"
                    cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, object_color, 2)

                    # Drawing the bbox
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), object_color, 2)

            output_video_frames.append(frame)

        return output_video_frames