from ultralytics import YOLO
import cv2
import os

class Tracker:

    def __init__(self):
        self.model = YOLO("yolov8x.pt")

    def process_video(self, frames, output_dir="detected_objects"):
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        detections = []
        output_video_frames = []

        color_dict = {
            "car": (0, 255, 0),
            "bus": (0, 0, 255),
            "truck": (255, 0, 0),
            "motorcycle": (255, 255, 0),
            "bicycle": (0, 255, 255)
        }

        valid_classes = ["car", "bus", "truck", "motorcycle", "bicycle"]

        for frame_idx, frame in enumerate(frames):
            results = self.model.track(frame, persist=True)[0]
            name_dict = results.names
            frame_detections = {}

            for box_idx, box in enumerate(results.boxes):
                track_id = int(box.id.tolist()[0])
                result = box.xyxy.tolist()[0]
                object_class_id = box.cls.tolist()[0]
                object_class_name = name_dict[object_class_id]

                if object_class_name in valid_classes:
                    frame_detections[track_id] = {object_class_name: result}

                    object_color = color_dict[object_class_name]
                    x1, y1, x2, y2 = map(int, result)
                    label = f"{object_class_name} {track_id}"

                    # Draw label and bounding box on the frame
                    cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, object_color, 2)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), object_color, 2)

                    # Crop the detected object
                    cropped_object = frame[y1:y2, x1:x2]

                    # Save the cropped object as an image
                    object_filename = f"{output_dir}/{object_class_name}_frame{frame_idx}_id{track_id}_box{box_idx}.jpg"
                    cv2.imwrite(object_filename, cropped_object)

            detections.append(frame_detections)
            output_video_frames.append(frame)

            # Display the processed frame
            cv2.namedWindow("Processed Frame", cv2.WINDOW_NORMAL)
            cv2.imshow('Processed Video Frame', frame)

            # Wait for a short duration and break if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Close all OpenCV windows
        cv2.destroyAllWindows()

        return output_video_frames