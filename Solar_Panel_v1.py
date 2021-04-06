


class solar_panel():

    def __init__(self,  Area, age, mass,  BoL_eff, inherent_deg, deg_Factor, efficiency, P_out, Spec_E):
        self.Area = Area
        self.Spec_E= Spec_E
        self.age = age -1/12
        self.inherent_deg = inherent_deg
        self.deg_Factor = deg_Factor
        self.BoL_eff = BoL_eff
        self.efficiency = efficiency
        self.P_out = P_out
        self.mass = 0.92*1418*self.BoL_eff*self.inherent_deg*(1-self.deg_Factor)**15*self.Area/self.Spec_E

    def __repr__(self):
        return ' Area: {0}, Age: {1}, Efficiency: {2}, Power Output: {3}'.format(self.Area,self.age, self.efficiency, self.P_out)

    def update(self):
        self.age += 1/12
        self.efficiency = self.BoL_eff*self.inherent_deg*(1-self.deg_Factor)**self.age #((1-self.inherent_deg)**self.age )
        self.P_out = self.efficiency*0.92*1418*self.Area/1000
        return self.age, self.efficiency, self.P_out




