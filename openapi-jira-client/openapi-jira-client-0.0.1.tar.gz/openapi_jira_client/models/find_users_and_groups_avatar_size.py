from enum import Enum


class FindUsersAndGroupsAvatarSize(str, Enum):
    XSMALL = "xsmall"
    X_S_M_A_L_L2_X = "xsmall@2x"
    X_S_M_A_L_L3_X = "xsmall@3x"
    SMALL = "small"
    S_M_A_L_L2_X = "small@2x"
    S_M_A_L_L3_X = "small@3x"
    MEDIUM = "medium"
    M_E_D_I_U_M2_X = "medium@2x"
    M_E_D_I_U_M3_X = "medium@3x"
    LARGE = "large"
    L_A_R_G_E2_X = "large@2x"
    L_A_R_G_E3_X = "large@3x"
    XLARGE = "xlarge"
    X_L_A_R_G_E2_X = "xlarge@2x"
    X_L_A_R_G_E3_X = "xlarge@3x"
    XXLARGE = "xxlarge"
    X_X_L_A_R_G_E2_X = "xxlarge@2x"
    X_X_L_A_R_G_E3_X = "xxlarge@3x"
    XXXLARGE = "xxxlarge"
    X_X_X_L_A_R_G_E2_X = "xxxlarge@2x"
    X_X_X_L_A_R_G_E3_X = "xxxlarge@3x"

    def __str__(self) -> str:
        return str(self.value)
