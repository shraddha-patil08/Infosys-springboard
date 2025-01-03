from ultralytics import YOLO
import cv2
import random
import os

class Tracker:

    def __init__(self):
        self.model = YOLO("yolo11x.pt")

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
        print(results)
        # print(results)
        name_dict = results.names
        shape = results.orig_shape
        print(shape)

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

        cy1 = 1100
        offset = 6

        counter = 0
        track_ids = []

        for frame, obj_detected in zip(frames, object_detections):

            for track_id, obj_details in obj_detected.items():

                for object_class, bbox in obj_details.items():

                    x1,y1,x2,y2 = bbox
                    self.save_objects(frame, x1,y1,x2,y2,track_id)

                    object_color = color_dict.get(object_class, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))

                    # center point
                    cx = int(x1 + x2) // 2
                    cy = int(y1 + y2) // 2  #1105

                    cv2.circle(frame, (cx, cy), 4, (255, 0, 0), -1)

                    #
                    cv2.line(frame, (450, 1100), (2100, 1100), (255, 255, 255), 1)

                    # Put text on the bbox
                    label = f"{object_class} {track_id}"

                    cv2.putText(frame, label, (int(x1), int(y1)-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, object_color, 2)

                    # vehicle number
                    total_vehicle = f"Vehicles No.: {counter}"
                    cv2.putText(frame, total_vehicle, (int(2100), int(30)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                    # Drawing the bbox
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), object_color, 2)

                    # if cy1<(cy) and cy1>(cy-offset):
                    if cy1<cy:

                        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

                        if track_id not in track_ids:
                            track_ids.append(track_id)
                            counter += 1



            cv2.imshow("RGB", frame)
            output_video_frames.append(frame)

        
        return output_video_frames

    # def save_objects(frame, x1, y1, x2, y2, obj_id, save_directory="data/output"):
    #     # Ensure save_directory is a string or path
    #     if not isinstance(save_directory, (str, os.PathLike)):
    #         raise TypeError(
    #             f"save_directory must be a string or os.PathLike object, not {type(save_directory).__name__}")
    #
    #     # Create the directory if it doesn't exist
    #     os.makedirs("data/output", exist_ok=True)
    #
    #     # Ensure the coordinates are scalar values
    #     x1, y1, x2, y2 = map(lambda v: int(v.item() if hasattr(v, "item") else v), [x1, y1, x2, y2])
    #
    #     # Crop the frame
    #     license_plate_crop = frame[int(y1):int(y2), int(x1): int(x2), :]
    #
    #     # Generate a unique filename
    #     filename = os.path.join(save_directory, f"object_{obj_id}_{len(os.listdir(save_directory)) + 1}.png")
    #
    #     # Save the cropped image
    #     cv2.imwrite(filename, crop)
    #     print(f"Colored image saved at: {filename}")