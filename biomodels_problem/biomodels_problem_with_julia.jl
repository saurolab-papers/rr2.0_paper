using SBMLToolkit, ModelingToolkit

fname = "D:\\roadrunner\\roadrunner\\test\\PerformanceTests\\biomodels_problem\\biomodels\\BIOMD0000000005.xml"
SBMLToolkit.checksupport(fname)
mdl = readSBML(fname, doc -> begin
    set_level_and_version(3, 2)(doc)
    convert_simplify_math(doc)
end)

rs = ReactionSystem(mdl)

# odesys = convert(ODESystem, rs)

# tspan = [0., 1.]
# prob = ODEProblem(odesys, [], tspan, [])
# sol = solve(prob, Tsit5())
