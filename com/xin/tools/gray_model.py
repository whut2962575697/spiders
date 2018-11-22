# -*- encoding:utf-8 -*-
import numpy as np
import math



def calculate_generate_list(input_list):
    generated_list = list()
    for k in range(len(input_list)):
        generate_x = 0
        for i in range(k+1):
            generate_x = generate_x + input_list[i]
        generated_list.append(generate_x)
    return generated_list


def calculate_neighbour_generate_list(input_list, p):
    generated_list = list()
    for k in range(1, len(input_list)):
        generate_x = input_list[k]*(1-p)+input_list[k-1]*p
        generated_list.append(generate_x)
    return generated_list


def calculate_gm(original_input, neighbour_generate_list, lamd):
    Y = np.transpose(np.array(original_input[1:]))
    b1 = -1*np.transpose(neighbour_generate_list)
    b2 = [z**lamd for z in neighbour_generate_list]
    b = [b1,b2]
    B = np.transpose(np.array(b))
    BTB = np.linalg.inv(np.matmul(np.transpose(B), B))
    u = np.matmul(np.matmul(BTB, np.transpose(B)), Y)
    return u


def gm(u, generated_list, lamd):
    a = u[0]
    b = u[1]

    predict_list = [generated_list[0]]
    for k, xk in enumerate(generated_list):
        _xk = ((b/a)+(generated_list[0]**(1-lamd)-b/a)*math.exp(-1*(1-lamd)*a*k))**(1/(1-lamd))
        predict_list.append(_xk)
    return predict_list


def reduct_list(predict_list):
    reductd_list = []
    for k in range(1,len(predict_list)):
        reduct_xk = predict_list[k] - predict_list[k-1]
        reductd_list.append(reduct_xk)
    return reductd_list


def calculate_residual(original_input, reducted_list):
    residual_list = []
    for k in range(1,len(original_input)):
        residual_list.append(original_input[k]-reducted_list[k])
    return residual_list


def modify_residual(residual_list):
    T = len(residual_list)
    Y = np.transpose(np.array(residual_list))
    P = []
    z = int(len(residual_list)/2-1)
    p1 = []
    for k in range(len(residual_list)):
        p1.append(0.5)
    P.append(p1)
    for m in range(z):
        p_1 = []
        p_2 = []
        for k in range(len(residual_list)):
            p_1.append(math.cos(2*math.pi*(m+1)/T*(k+2)))
            p_2.append(math.sin(2*math.pi*(m+1)/T*(k+2)))
        P.append(p_1)
        P.append(p_2)
    P = np.transpose(P)
    PTP = np.linalg.inv(np.matmul(np.transpose(P), P))
    c = np.matmul(np.matmul(PTP, np.transpose(P)), Y)
    new_residual_list = []
    for k, residual in enumerate(residual_list):
        new_residual = 0.5*c[0]
        for m in range(z):
            new_residual = new_residual+c[1+2*m]*math.cos(2*math.pi*(m+1)/T*(k+2))+c[1+2*m+1]*math.sin(2*math.pi*(m+1)/T*(k+2))
            new_residual_list.append(new_residual)
    return new_residual_list


def modify_gm(new_residual_list, reducted_list):
    new_predicted_list = []
    for k, predictd_x in enumerate(reducted_list[1:]):
        new_predicted_list.append(predictd_x+new_residual_list[k])
    return new_predicted_list


def main(original_input, lamd, p):
    # original_input = [2646, 3684, 3564, 2493, 3595]
    generated_list = calculate_generate_list(original_input)
    neighbour_generated_list = calculate_neighbour_generate_list(generated_list, p)
    u = calculate_gm(original_input, neighbour_generated_list, lamd)
    predicted_list = gm(u, generated_list, lamd)
    reducted_list = reduct_list(predicted_list)
    residual_list = calculate_residual(original_input, reducted_list)
    new_residual_list = modify_residual(residual_list)
    final_predict = modify_gm(new_residual_list, reducted_list)
    return final_predict

if __name__ == "__main__":
    original_input = [2646, 3684, 3564, 2493, 3595]
    print (main(original_input, 2.2516138703592947, 0.14546803563696983))
    # generated_list = calculate_generate_list(original_input)
    # neighbour_generated_list = calculate_neighbour_generate_list(generated_list, 0.14546803563696983)
    # u = calculate_gm(original_input, neighbour_generated_list, 2.2516138703592947)
    # predicted_list = gm(u, generated_list, 2.2516138703592947)
    # reducted_list = reduct_list(predicted_list)
    # residual_list = calculate_residual(original_input, reducted_list)
    # new_residual_list = modify_residual(residual_list)
    # final_predict = modify_gm(new_residual_list, reducted_list)
    # print (final_predict)

