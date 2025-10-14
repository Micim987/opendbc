
from opendbc.car import structs
from opendbc.car.honda.values import CarControllerParams, HONDA_BOSCH
from opendbc.sunnypilot.car.honda.values_ext import CarControllerParamsExt
import numpy as np


class CarInterfaceExt:
  def __init__(self, CP: structs.CarParams, CP_SP: structs.CarParamsSP):
    self.CP = CP
    self.CP_SP = CP_SP

  @staticmethod
  def get_pid_accel_limits(CP, CP_SP, current_speed, cruise_speed):
    if CP.carFingerprint in HONDA_BOSCH:
      return CarControllerParams.BOSCH_ACCEL_MIN, CarControllerParams.BOSCH_ACCEL_MAX
    elif CP.carFingerprint not in HONDA_BOSCH and CP_SP.enableGasInterceptor:
      return CarControllerParamsExt.NIDEC_PEDAL_ACCEL_MIN, CarControllerParamsExt.NIDEC_PEDAL_ACCEL_MAX
    else:
      # NIDECs don't allow acceleration near cruise_speed,
      # so limit limits of pid to prevent windup
      ACCEL_MAX_VALS = [CarControllerParams.NIDEC_ACCEL_MAX, 0.2]
      ACCEL_MAX_BP = [cruise_speed - 2., cruise_speed - .2]
      return CarControllerParams.NIDEC_ACCEL_MIN, np.interp(current_speed, ACCEL_MAX_BP, ACCEL_MAX_VALS)