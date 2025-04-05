import torch
import numpy as np
import cv2
import face_alignment
from scipy.spatial.transform import Rotation
import dlib
import os

class DreamActorInference:
    def __init__(self):
        """אתחול מודל DreamActor"""
        # טעינת המודל המאומן
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self._load_model()
        
        # אתחול מזהה פנים ונקודות ציון
        self.face_detector = dlib.get_frontal_face_detector()
        self.fa = face_alignment.FaceAlignment(face_alignment.LandmarksType._2D, device=self.device)
        
    def _load_model(self):
        """טעינת המודל המאומן"""
        model_path = os.path.join(os.path.dirname(__file__), 'checkpoints/model.pth')
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                "קובץ המודל לא נמצא. אנא הורד את המודל המאומן מ: "
                "https://github.com/OpenTalker/DreamTalk/releases"
            )
        
        model = torch.load(model_path, map_location=self.device)
        model.eval()
        return model
    
    def _extract_face_landmarks(self, image):
        """חילוץ נקודות ציון מהפנים"""
        # זיהוי פנים
        faces = self.face_detector(image)
        if len(faces) == 0:
            raise ValueError("לא זוהו פנים בתמונה")
            
        # חילוץ נקודות ציון
        landmarks = self.fa.get_landmarks(image)
        if landmarks is None or len(landmarks) == 0:
            raise ValueError("לא ניתן לחלץ נקודות ציון מהפנים")
            
        return landmarks[0]  # מחזיר את נקודות הציון של הפנים הראשונות שזוהו
        
    def _process_audio(self, audio_path):
        """עיבוד האודיו לייצוג שניתן להזין למודל"""
        # TODO: להוסיף עיבוד אודיו אמיתי
        # כרגע מחזיר מערך אקראי לדוגמה
        return np.random.randn(128, 32)  # ייצוג אודיו מדומה
        
    def animate_image(self, image, audio_path):
        """יצירת אנימציה מתמונה ואודיו"""
        try:
            # חילוץ נקודות ציון מהפנים
            landmarks = self._extract_face_landmarks(image)
            
            # עיבוד האודיו
            audio_features = self._process_audio(audio_path)
            
            # המרה לטנסורים
            image_tensor = torch.from_numpy(image).float().to(self.device)
            landmarks_tensor = torch.from_numpy(landmarks).float().to(self.device)
            audio_tensor = torch.from_numpy(audio_features).float().to(self.device)
            
            # יצירת האנימציה
            with torch.no_grad():
                animated_frames = self.model(
                    image_tensor.unsqueeze(0),
                    landmarks_tensor.unsqueeze(0),
                    audio_tensor.unsqueeze(0)
                )
            
            # המרה חזרה למערך נאמפיי
            animated_frames = animated_frames.cpu().numpy()
            
            # נרמול התמונות
            animated_frames = (animated_frames * 255).astype(np.uint8)
            
            return animated_frames
            
        except Exception as e:
            raise Exception(f"שגיאה ביצירת האנימציה: {str(e)}") 