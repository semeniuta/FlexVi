# FlexVi

FlexVi ("flexibility through vision") is an open souce library for the research in robot vision systems calibration and other machine vision tasks. 

## Library structure

| Package | Description |
| --- | --- |
| flexvi | The root package |
| flexvi.calibration | Vision calibration functionality |
| flexvi.calibration.containers | Classes-containers related to vision calibration |
| flexvi.calibration.ti | Modules related to identification of “true intrinsics” |
| flexvi.confmanager | Management of configuration files |
| flexvi.dataanalysis | Modules used for data analysis and statistical operations |
| flexvi.handeye | Hand-eye calibration functionality |
| flexvi.handeye.hecalibrators | Hand-eye calibrator classes |
| flexvi.handeye.outliers | Modules related to the removal of outliers from the movement data |
| flexvi.opencv | Modules providing interaction with OpenCV library |
| flexvi.transform | Modules dealing with homogeneous transformations |

## Usage of the calibrators (`flexvi.calibration` package)

### CameraCalibrator

Simple camera calibration using a predefined set of images or all images from the set.

Usage:
```python
cal = CameraCalibrator(imset)
cal.calibrate()
```

To access the results:
`cal.calib_res` - raw OpenCV calibration result
`cal.camera` - parametrized Camera object
`cal.camera_matrix`, `cal.dist_coefs` - accesing the intrinsics separately

### StereoVisionSystemCalibrator

Usage:
```python
cfinder = ChessboardCornersFinder(imset1, imset2)
cal = StereoVisionSystemCalibrator(cfinder)
cal.calibrate()
```

To access the results:
`cal.svs` - parametrized StereoVisionSystem object

### FixedPoseCalibrator

Fixed pose calibrator. Determines a transformation between a fixed object (e.g. a feeder) and
a camera

Usage:
```python
cal = FixedPoseCalibrator(img, pattern_size, square_size, intrinsics)
cal.calibrate()
```
To access the results:
`cal.rotation`
`cal.translation`
`cal.homography_matrix`
