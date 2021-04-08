import torch

from metlibvi.callbacks import on_transition_end_callback
from metlibvi.mcmc import get_acceptance_ratio


def vanilla_vi_forward(transitions, z, x=None, **kwargs):
    """
    The function implements forward step for vanilla variational inference
    :param transitions: transitions, represented ad a Modulelist
    :param z: a batch of initial (not yet transformed) samples (e.g. from standard normal)
    :param x: a batch of data objects (if any)
    :return: returns mean KL divergence
    """

    output = transitions(z.clone())
    final_samples, sum_log_jac = output["z_new"], output["aggregated_log_jac"]

    return {"z_new": final_samples, "aggregated_log_jac": sum_log_jac}


def transition_forward_aux(transition, input_dict):
    if transition.name == "RealNVP":
        with torch.no_grad():
            prob = torch.sigmoid(input_dict["forward_logit_prob"])
            rand = torch.rand_like(prob)
            move_forward = rand < prob.squeeze()
        f = transition(**input_dict)
        b = transition.inverse(**input_dict)

        f["forward_logit_prob"] = input_dict["forward_logit_prob"]
        b["forward_logit_prob"] = -input_dict["forward_logit_prob"]

        output = apply_acceptance(current_state=b, proposal_state=f, decisions=move_forward)
        # this is to simplify log acceptance computation. There should be + or - forward logit
        multiplier = move_forward * 2. - 1.
    else:
        output = transition(**input_dict)
        output["forward_logit_prob"] = input_dict["forward_logit_prob"]
        multiplier = torch.ones_like(output["z_new"][:, 0])
    return output, multiplier


def apply_decision_unit(current, proposed, decisions):
    res = torch.empty_like(current)
    res[decisions] = proposed[decisions]
    res[~decisions] = current[~decisions]
    return res


def apply_acceptance(current_state, proposal_state, decisions):
    result = {}
    for k in current_state.keys():
        result[k] = apply_decision_unit(current_state[k], proposal_state[k], decisions)

    return result


def metropolized_vi_forward(transitions, target_logprob, z, x=None, forward_logit_prob=None,
                            accept_reject_correction=True,
                            use_barker=False, **kwargs):
    """
    The function returns forward step for metropolized vi
    :param transitions: transitions, represented ad a Modulelist
    :param target_logprob: a function, which computes target's logprob
    :param forward_logit_prob: a vector of length len(transitions), which contains logit probabilities of forward transitions
    :param z: a batch of initial (not yet transformed) samples (e.g. from standard normal)
    :param x: a batch of data objects (if any)
    :param use_barker: whether to use barker ratio or not
    :return: returns loss (precomputed grad) for metropolized algorithms
    """
    if forward_logit_prob is None:
        forward_logit_prob = torch.zeros(len(transitions))

    sum_log_alphas = torch.zeros_like(z[:, 0])
    sum_log_jac = torch.zeros_like(z[:, 0])
    sum_log_probs = torch.zeros_like(z[:, 0])

    z_cur = z.clone()

    for i in range(len(transitions)):
        input_dict = {"z": z_cur, "target_logprob": target_logprob, "x": x,
                      "forward_logit_prob": forward_logit_prob[i] * torch.ones_like(z[:, 0])}
        output, multiplier = transition_forward_aux(transition=transitions[i], input_dict=input_dict)

        target_log_density_upd = target_logprob(z=output["z_new"], x=x)
        target_log_density_old = target_logprob(z=z, x=x)

        log_t = target_log_density_upd - target_log_density_old - input_dict["forward_logit_prob"] * multiplier + \
                output["aggregated_log_jac"] + output.get("aux_for_acceptance_ratio", torch.zeros_like(z[:, 0]))
        log_1pt = torch.logsumexp(torch.cat([torch.zeros_like(log_t).view(-1, 1),
                                             log_t.view(-1, 1)], dim=-1), dim=-1)

        a, current_log_alphas, acceptance_log_alphas = get_acceptance_ratio(log_t, log_1pt, use_barker=use_barker)

        if accept_reject_correction:
            current_state = {"z_new": z_cur, "aggregated_log_jac": torch.zeros_like(z[:, 0]),
                             "forward_logit_prob": input_dict["forward_logit_prob"]}
            resulting_dict = apply_acceptance(current_state=current_state, proposal_state=output, decisions=a)
        else:
            resulting_dict = output

        sum_log_alphas = sum_log_alphas + current_log_alphas
        sum_log_jac = sum_log_jac + resulting_dict["aggregated_log_jac"]
        sum_log_probs = sum_log_probs + torch.log(torch.sigmoid(resulting_dict["forward_logit_prob"]))

        on_transition_end_callback(z_accepted=resulting_dict["z_new"], z_proposal=output["z_new"],
                                   acceptance_logprobs=current_log_alphas,
                                   **kwargs)

        z_cur = resulting_dict["z_new"]

    return {"z_new": z_cur, "aggregated_log_jac": sum_log_jac, "sum_log_probs": sum_log_probs,
            "sum_log_alphas": sum_log_alphas, }
