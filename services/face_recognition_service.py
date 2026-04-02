"""Face recognition service for voter authentication"""
import cv2
import numpy as np
from pathlib import Path
import pickle
from typing import Optional, Tuple
import os

class FaceRecognitionService:
    """Service for face recognition authentication"""
    
    def __init__(self, data_dir: str = "face_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.face_encodings = {}
        self.load_face_data()
    
    def load_face_data(self):
        """Load saved face encodings"""
        face_data_file = self.data_dir / "face_encodings.pkl"
        if face_data_file.exists():
            with open(face_data_file, 'rb') as f:
                self.face_encodings = pickle.load(f)
    
    def save_face_data(self):
        """Save face encodings to file"""
        face_data_file = self.data_dir / "face_encodings.pkl"
        with open(face_data_file, 'wb') as f:
            pickle.dump(self.face_encodings, f)
    
    def capture_face(self) -> Optional[np.ndarray]:
        """
        Capture face from webcam
        Returns: face image array or None
        """
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("❌ Không thể mở webcam. Vui lòng kiểm tra:")
                print("   - Webcam đã được kết nối")
                print("   - Không có ứng dụng nào khác đang sử dụng webcam")
                print("   - Quyền truy cập camera đã được cấp")
                return None
            
            face_img = None
            print("📸 Nhấn SPACE để chụp, ESC để hủy")
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("❌ Không thể đọc frame từ webcam")
                    break
                
                # Detect faces
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                # Draw rectangle around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                # Display instructions
                cv2.putText(frame, "Press SPACE to capture, ESC to cancel", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('Face Capture', frame)
                
                key = cv2.waitKey(1)
                if key == 27:  # ESC
                    print("❌ Đã hủy chụp ảnh")
                    break
                elif key == 32:  # SPACE
                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        face_img = frame[y:y+h, x:x+w]
                        print("✅ Đã chụp khuôn mặt")
                        break
                    else:
                        print("⚠️ Không phát hiện khuôn mặt. Vui lòng thử lại.")
                
                frame_count += 1
                
        except Exception as e:
            print(f"❌ Lỗi khi chụp ảnh: {str(e)}")
            return None
        finally:
            try:
                cap.release()
                cv2.destroyAllWindows()
            except:
                pass
        
        return face_img
    
    def register_face(self, cccd: str, name: str) -> bool:
        """
        Register a new face for a voter
        Args:
            cccd: Citizen ID number
            name: Voter name
        Returns: True if successful
        """
        print(f"🎯 Đăng ký khuôn mặt cho {name} (CCCD: {cccd})")
        face_img = self.capture_face()
        
        if face_img is None:
            print("❌ Không thể chụp khuôn mặt")
            return False
        
        # Convert to grayscale and resize
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (100, 100))
        
        # Store face encoding (simplified - using raw pixels)
        self.face_encodings[cccd] = {
            'encoding': resized.flatten(),
            'name': name,
            'image_shape': resized.shape
        }
        
        # Save face image
        face_img_path = self.data_dir / f"{cccd}.jpg"
        cv2.imwrite(str(face_img_path), face_img)
        
        self.save_face_data()
        print(f"✅ Đã đăng ký khuôn mặt cho {name}")
        return True
    
    def verify_face(self, cccd: str, threshold: float = 0.6) -> Tuple[bool, float]:
        """
        Verify face against registered face
        Args:
            cccd: Citizen ID to verify against
            threshold: Similarity threshold (0-1)
        Returns: (is_match, confidence)
        """
        if cccd not in self.face_encodings:
            print(f"❌ CCCD {cccd} chưa đăng ký khuôn mặt")
            return False, 0.0
        
        print(f"🔍 Xác thực khuôn mặt cho CCCD: {cccd}")
        face_img = self.capture_face()
        
        if face_img is None:
            print("❌ Không thể chụp khuôn mặt")
            return False, 0.0
        
        # Convert and resize
        gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (100, 100))
        current_encoding = resized.flatten()
        
        # Compare with stored encoding
        stored_encoding = self.face_encodings[cccd]['encoding']
        
        # Calculate similarity (normalized correlation)
        similarity = np.corrcoef(current_encoding, stored_encoding)[0, 1]
        confidence = (similarity + 1) / 2  # Normalize to 0-1
        
        is_match = confidence >= threshold
        
        if is_match:
            print(f"✅ Xác thực thành công! Độ tin cậy: {confidence:.2%}")
        else:
            print(f"❌ Xác thực thất bại! Độ tin cậy: {confidence:.2%}")
        
        return is_match, confidence
    
    def has_registered_face(self, cccd: str) -> bool:
        """Check if CCCD has registered face"""
        return cccd in self.face_encodings
    
    def delete_face(self, cccd: str) -> bool:
        """Delete registered face data"""
        if cccd in self.face_encodings:
            del self.face_encodings[cccd]
            
            # Delete image file
            face_img_path = self.data_dir / f"{cccd}.jpg"
            if face_img_path.exists():
                face_img_path.unlink()
            
            self.save_face_data()
            return True
        return False
