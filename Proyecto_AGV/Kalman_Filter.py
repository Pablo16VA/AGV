import numpy as np
#Initialize covariance matrix
P = 1000*np.eye(3)

x = np.zeros((3,1)) # State matrix [x, y, theta]^T
theta = 0
omega = 0
u = np.zeros((2,1)) # Control array, need to parse linear velocity and angular velocity 

def kalman_filter(P,x,u):
    #Define measurement vector
    Z_gps = np.array([[1],      #Replace values with data from GPS
                      [1]])
    
    dt = 1 #time step 
    #State transition matrix 
    F =np.eye(3) #Identity matrix for the state transition matrix, see mathematical model for further reference

    #Control matrix
    G = np.array([[dt*np.cos(theta+omega*dt/2), 0],  #Need to define theta via mathematical equation using omega, omega will be given by gyroscope
                [dt*np.sin(theta+omega*dt/2), 0],
                [0, dt]])

    #Measurement matrix
    H = np.array([[1, 0, 0],
                [0, 1, 0]])  #Theta is not measureable 

    # Define process noise covariance matrix
    q = 0.1
    Q = q*G@G.T 

    #Define measurement noise covariance matrix
    r_gps = 0.1 #The GPS used is precise, therefore a low measurement noise
    r_gyro = 1  #The gyroscope's accuracy is not well documented, so assume a bigger value

    R = np.array([[r_gps, 0],
                [0, r_gps]])
    #Define Kalman Gain
    K = P@H.T@np.linalg.inv(H@P@H.T + R)
    #Update estimate of states with measurement
    x = x + K@(Z_gps-H@x)
    #Update estimate uncertainty
    P = (np.eye(3)-K@H) @ P @ (np.eye(3)-K@H).T + K@R@K.T

    #Prediction step 

    #Extrapolate state
    x = F@x + G@u
    #Extrapolate uncertainty 
    P = F@P@F.T + Q





