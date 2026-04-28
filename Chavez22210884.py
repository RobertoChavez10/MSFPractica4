"""
Práctica 4: Sistema Endocrino

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Chávez González Roberto
Número de control: 22210884
Correo institucional: l22210884@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# librerías
import numpy as np
import matplotlib.pyplot as plt
import control as ctrl

# datos de la simulación
x0, t0, tend, dt, w, h = 0, 0, 10, 1E-3, 7, 3.5
N = int(tend/dt) + 1
t = np.linspace(t0, tend, N)
u2 = np.zeros(N); u2[round(1/dt):] = 1  # Step

# parámetros del circuito
R1 = 1e3
L  = 100e-3
R2 = 1e3
C  = 100e-6

# función de transferencia
Num = [1e3]
Den = [(1000e-6*100e-3*1e3), (1000e-6*1e3*1e3 + 100e-3), (1e3 + 1e3)]

sys_ctrl = ctrl.tf(Num, Den)
sys_caso = ctrl.tf(Num, Den)
print(f"FT Control: {sys_ctrl}\n")
print(f"FT Caso:    {sys_caso}\n")

# controlador PID
def controlador(kP, kI, kD, sys):
    Cr = 1e-6
    Re = 1 / (kI * Cr)
    Rr = kP * Re
    Ce = kD / Rr
    numPID = [Re*Rr*Ce*Cr, (Re*Ce + Rr*Cr), 1]
    denPID = [Re*Cr, 0]
    PID = ctrl.tf(numPID, denPID)
    print(f"FT Controlador PID: {PID}\n")
    X      = ctrl.series(PID, sys)
    sysPID = ctrl.feedback(X, 1, sign=-1)
    return sysPID

kP = 139.024398952871

kI = 3579.00250163921

kD = 0.182003845761544

sys_caso_LC = controlador(kP, kI, kD, sys_caso)
print(f"FT Caso LC: {sys_caso_LC}\n")

# respuestas
_, F_ctrl   = ctrl.forced_response(sys_ctrl,    t, u2, x0) 
 
_, F_caso   = ctrl.forced_response(sys_caso,    t, u2, x0) 
 
_, PID_caso = ctrl.forced_response(sys_caso_LC, t, u2, x0)  

# colores
clr1 = [0.12, 0.43, 0.19]  

clr2 = [0.85, 0.35, 0.05]  

clr3 = [0.09, 0.37, 0.65]  

# gráfica: scope de saso
fig, ax = plt.subplots(1, 1, figsize=(w, h))
fig.patch.set_facecolor('white')

ax.plot(t, u2,      '-',  color=clr1, linewidth=1.5, label=r'$V_s(t):\ Control$')

ax.plot(t, F_caso,  '-',  color=clr2, linewidth=1.0, label=r'$V_s(t):\ Caso$')

ax.plot(t, PID_caso,':',  color=clr3, linewidth=2.0, label=r'$PID$')

ax.set_xlim(0, 10); ax.set_xticks(np.arange(0, 11, 1))
ax.set_ylim(0, 1.2); ax.set_yticks(np.arange(0, 1.4, 0.2))
ax.set_xlabel(r'$t\ [s]$', fontsize=12)
ax.set_ylabel(r'$V_s(t)\ [V]$', fontsize=12)
ax.set_title('Scope de Caso', fontsize=12, fontweight='bold')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.25), ncol=3,
          fontsize=9, frameon=False)

plt.tight_layout()
plt.savefig('endocrino.pdf', bbox_inches='tight')
plt.show()