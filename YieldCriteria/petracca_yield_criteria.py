import tensorflow as tf
import numpy as np

from ConLawLearn.YieldCriteria.yield_criteria_utilities import YieldCriteriaUtilities

def NegativeEquivalentStressPetracca(SIG_EFF, fc0, fcp, fcbi, ft):
    with tf.name_scope("PetraccaYieldNegative"):
        k1 = tf.constant(0.16)

        kb      = YieldCriteriaUtilities.Kb(fcbi, fcp)
        alpha   = YieldCriteriaUtilities.Alpha(kb)
        beta    = YieldCriteriaUtilities.Beta(fc0, ft, alpha)
        i1      = YieldCriteriaUtilities.FirstInvariant(SIG_EFF)
        j2      = YieldCriteriaUtilities.SecondDeviatoricInvariant(SIG_EFF)
        s1, s2  = YieldCriteriaUtilities.PrincipalStressValues(SIG_EFF)
        s_max   = YieldCriteriaUtilities.PrincipalStressMax(s1, s2)
        s_min_heavi = YieldCriteriaUtilities.PrincipalStressMinHeaviside(s1,s2)

        ratio1  = YieldCriteriaUtilities.AlphaRatio(alpha)
        term1   = YieldCriteriaUtilities.AuxTerm1(alpha, i1)
        term2   = YieldCriteriaUtilities.AuxTerm2(j2)
        term3   = YieldCriteriaUtilities.AuxTerm3(s_max, beta)

        tau = tf.multiply(tf.multiply(ratio1, tf.add(tf.add(term1, term2),\
                                         tf.multiply(k1,term3))),s_min_heavi)
    return tau

def PositiveEquivalentStressPetracca(SIG_EFF, fcp, fcbi, ft):
    with tf.name_scope("PetraccaYieldNegative"):
        kb      = YieldCriteriaUtilities.Kb(fcbi, fcp)
        alpha   = YieldCriteriaUtilities.Alpha(kb)
        beta    = YieldCriteriaUtilities.Beta(fcp, ft, alpha)
        i1      = YieldCriteriaUtilities.FirstInvariant(SIG_EFF)
        j2      = YieldCriteriaUtilities.SecondDeviatoricInvariant(SIG_EFF)
        s1, s2  = YieldCriteriaUtilities.PrincipalStressValues(SIG_EFF)
        s_max   = YieldCriteriaUtilities.PrincipalStressMax(s1, s2)
        s_max_heavi = YieldCriteriaUtilities.PrincipalStressMaxHeaviside(s1,s2)

        ratio1  = YieldCriteriaUtilities.AlphaRatio(alpha)
        ratio2  = YieldCriteriaUtilities.TensionCompressionRatio(ft, fcp)
        term1   = YieldCriteriaUtilities.AuxTerm1(alpha, i1)
        term2   = YieldCriteriaUtilities.AuxTerm2(j2)
        term3   = YieldCriteriaUtilities.AuxTerm3(s_max, beta)

        tau = tf.multiply(tf.multiply(tf.multiply(ratio1, tf.add(term1, tf.add(term2,term3))) \
                      ,ratio2), s_max_heavi)
        return tau


    return tau
