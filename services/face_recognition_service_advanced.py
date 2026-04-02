"""Advanced Face Recognition Service with Deep Learning and Liveness Detection"""
import cv2
import numpy as np
from pathlib import Path
import pickle
from typing import Optional, Tuple
import os
import time

try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    print("⚠️ face_recognition not available, using fallback mode")

class FaceRecognitionServiceAdvanced:
    """Advanced service for face recognition with liveness detection"""
    
    def __init__(self, data_dir: str = "face_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
        self.eye_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_eye.xml'
        )
        self.face_encodings = {}
        self.load_face_data()
        self.use_advanced = FACE_RECOGNITION_AVAILABLE
    
    def load_face_data(self):
        """Load saved face encodings"""
        face_data_file = self.data_dir / "face_encodings_advanced.pkl"
        if face_data_file.exists():
            with open(face_data_file, 'rb') as f:
                self.face_encodings = pickle.load(f)
    
    def save_face_data(self):
        """Save face encodings to file"""
        face_data_file = self.data_dir / "face_encodings_advanced.pkl"
        with open(face_data_file, 'wb') as f:
            pickle.dump(self.face_encodings, f)
    
    def detect_blinks(self, cap, duration: int = 5) -> int:
        """
        Detect eye blinks for liveness detection
        Returns: number of blinks detected
        """
        print(f"👁️ Phát hiện nhấp nháy mắt trong {duration} giây...")
        print("   Vui lòng nhấp nháy mắt 2-3 lần")
        
        blink_count = 0
        eyes_closed_frames = 0
        eyes_open_frames = 0
        blink_threshold = 3  # Frames to consider as blink
        
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            eyes_detected = False
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
                
                if len(eyes) >= 2:
                    eyes_detected = True
                    eyes_open_frames += 1
                    if eyes_closed_frames >= blink_threshold:
                        blink_count += 1
                        print(f"   ✓ Phát hiện nhấp nháy #{blink_count}")
                    eyes_closed_frames = 0
                else:
                    eyes_closed_frames += 1
                    eyes_open_frames = 0
                
                # Draw rectangle
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.putText(frame, f"Blinks: {blink_count}", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Display instructions
            remaining = int(duration - (time.time() - start_time))
            cv2.putText(frame, f"Nhan nhay mat - Con {remaining}s", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, f"Blinks: {blink_count}/2", (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            cv2.imshow('Liveness Detection - Blink', frame)
            if cv2.waitKey(1) == 27:  # ESC
                break
        
        cv2.destroyWindow('Liveness Detection - Blink')
        return blink_count
    
    def detect_head_movement(self, cap, duration: int = 5) -> bool:
        """
        Detect head movement (left/right) for liveness detection
        Returns: True if movement detected
        """
        print(f"↔️ Phát hiện chuyển động đầu trong {duration} giây...")
        print("   Vui lòng quay đầu sang TRÁI, sau đó sang PHẢI")
        
        face_positions = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            ret, frame = cap.read()
            if not ret:
                break
            
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            for (x, y, w, h) in faces:
                center_x = x + w // 2
                face_positions.append(center_x)
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, y + h // 2), 5, (0, 0, 255), -1)
            
            # Display instructions
            remaining = int(duration - (time.time() - start_time))
            cv2.putText(frame, f"Quay dau trai/phai - Con {remaining}s", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            
            cv2.imshow('Liveness Detection - Movement', frame)
            if cv2.waitKey(1) == 27:  # ESC
                break
        
        cv2.destroyWindow('Liveness Detection - Movement')
        
        # Analyze movement
        if len(face_positions) < 10:
            return False
        
        # Check for significant left-right movement
        min_pos = min(face_positions)
        max_pos = max(face_positions)
        movement_range = max_pos - min_pos
        
        # Movement should be at least 50 pixels
        movement_detected = movement_range > 50
        
        if movement_detected:
            print(f"   ✓ Phát hiện chuyển động: {movement_range} pixels")
        else:
            print(f"   ✗ Chuyển động không đủ: {movement_range} pixels (cần >50)")
        
        return movement_detected
    
    def check_liveness(self, cap) -> Tuple[bool, str]:
        """
        Comprehensive liveness detection
        Returns: (is_alive, message)
        """
        print("\n🔍 BẮT ĐẦU KIỂM TRA LIVENESS")
        print("=" * 50)
        
        # Test 1: Blink detection
        blink_count = self.detect_blinks(cap, duration=5)
        if blink_count < 2:
            return False, f"Không đủ nhấp nháy mắt ({blink_count}/2). Vui lòng thử lại."
        
        print(f"✅ Test 1 passed: {blink_count} blinks detected")
        
        # Test 2: Head movement
        movement_detected = self.detect_head_movement(cap, duration=5)
        if not movement_detected:
            return False, "Không phát hiện chuyển động đầu. Vui lòng thử lại."
        
        print(f"✅ Test 2 passed: Head movement detected")
        print("=" * 50)
        print("✅ LIVENESS VERIFICATION PASSED\n")
        
        return True, "Xác thực liveness thành công"
    
    def capture_face_with_liveness(self) -> Optional[np.ndarray]:
        """
        Capture face with liveness detection
        Returns: face image array or None
        """
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                print("❌ Không thể mở webcam")
                return None
            
            # Step 1: Liveness detection
            is_alive, message = self.check_liveness(cap)
            if not is_alive:
                print(f"❌ Liveness check failed: {message}")
                cap.release()
                cv2.destroyAllWindows()
                return None
            
            # Step 2: Capture face
            print("📸 Nhấn SPACE để chụp, ESC để hủy")
            face_img = None
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, "Face Detected - Press SPACE", (x, y-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.putText(frame, "Press SPACE to capture, ESC to cancel", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow('Face Capture', frame)
                
                key = cv2.waitKey(1)
                if key == 27:  # ESC
                    break
                elif key == 32:  # SPACE
                    if len(faces) > 0:
                        x, y, w, h = faces[0]
                        face_img = frame[y:y+h, x:x+w]
                        print("✅ Đã chụp khuôn mặt")
                        break
            
            cap.release()
            cv2.destroyAllWindows()
            return face_img
            
        except Exception as e:
            print(f"❌ Lỗi: {str(e)}")
            return None
    
    def register_face(self, cccd: str, name: str) -> bool:
        """
        Register face with advanced deep learning
        """
        print(f"🎯 Đăng ký khuôn mặt cho {name} (CCCD: {cccd})")
        
        face_img = self.capture_face_with_liveness()
        if face_img is None:
            return False
        
        # Convert BGR to RGB for face_recognition library
        rgb_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        
        if self.use_advanced:
            # Use deep learning (128-D encoding)
            encodings = face_recognition.face_encodings(rgb_img)
            if len(encodings) == 0:
                print("❌ Không thể trích xuất face encoding")
                return False
            
            encoding = encodings[0]
            print(f"✅ Trích xuất 128-D face encoding (Deep Learning)")
        else:
            # Fallback: Use simple method
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (100, 100))
            encoding = resized.flatten()
            print(f"⚠️ Sử dụng phương pháp đơn giản (face_recognition chưa cài)")
        
        # Store encoding
        self.face_encodings[cccd] = {
            'encoding': encoding,
            'name': name,
            'method': 'deep_learning' if self.use_advanced else 'simple'
        }
        
        # Save face image
        face_img_path = self.data_dir / f"{cccd}_advanced.jpg"
        cv2.imwrite(str(face_img_path), face_img)
        
        self.save_face_data()
        print(f"✅ Đã đăng ký khuôn mặt cho {name}")
        return True
    
    def verify_face(self, cccd: str, threshold: float = 0.6) -> Tuple[bool, float]:
        """
        Verify face with liveness detection
        """
        if cccd not in self.face_encodings:
            print(f"❌ CCCD {cccd} chưa đăng ký khuôn mặt")
            return False, 0.0
        
        print(f"🔍 Xác thực khuôn mặt cho CCCD: {cccd}")
        
        face_img = self.capture_face_with_liveness()
        if face_img is None:
            return False, 0.0
        
        rgb_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
        stored_data = self.face_encodings[cccd]
        stored_encoding = stored_data['encoding']
        
        if self.use_advanced and stored_data.get('method') == 'deep_learning':
            # Use deep learning comparison
            current_encodings = face_recognition.face_encodings(rgb_img)
            if len(current_encodings) == 0:
                print("❌ Không thể trích xuất face encoding")
                return False, 0.0
            
            current_encoding = current_encodings[0]
            
            # Calculate face distance (lower is better)
            distance = face_recognition.face_distance([stored_encoding], current_encoding)[0]
            confidence = 1 - distance  # Convert to confidence (higher is better)
            
            # Stricter threshold for deep learning (0.4 instead of 0.6)
            is_match = distance < 0.4
            
            print(f"   Distance: {distance:.3f}, Confidence: {confidence:.2%}")
        else:
            # Fallback method
            gray = cv2.cvtColor(face_img, cv2.COLOR_BGR2GRAY)
            resized = cv2.resize(gray, (100, 100))
            current_encoding = resized.flatten()
            
            similarity = np.corrcoef(current_encoding, stored_encoding)[0, 1]
            confidence = (similarity + 1) / 2
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
            
            # Delete image files
            for suffix in ['_advanced.jpg', '.jpg']:
                face_img_path = self.data_dir / f"{cccd}{suffix}"
                if face_img_path.exists():
                    face_img_path.unlink()
            
            self.save_face_data()
            return True
        return False
