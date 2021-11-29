## Writing the output to the video itself for example sake 

import cv2

cap = cv2.VideoCapture(f'./test/goodtest/Good 2.mov')
out = cv2.VideoWriter_fourcc(*'XVID')
(grabbed, frame) = cap.read()
fshape = frame.shape
fheight = fshape[0]
fwidth = fshape[1]
print fwidth , fheight
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (fwidth,fheight))

while(True):
      
    # Capture frames in the video
    ret, frame = cap.read()
  
    # describe the type of font
    # to be used.
    font = cv2.FONT_HERSHEY_SIMPLEX
  
    text_to_display = f'This is a Bicep Curl exercise with 99% probability\n this is also an example of a good Bicep Curl'
    # Use putText() method for
    # inserting text on video
    cv2.putText(frame, 
                text_to_display, 
                (50, 50), 
                font, 1, 
                (0, 255, 255), 
                2, 
                cv2.LINE_4)
  
    # Display the resulting frame
    cv2.imshow('name',frame)
    out.write(frame)
  
    # creating 'q' as the quit 
    # button for the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# release the cap object
cap.release()
# close all windows
cv2.destroyAllWindows()