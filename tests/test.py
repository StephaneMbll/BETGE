import betge

for path in glob.glob("../Neuroscans_OCD_metacognition"):
    print(path)

epochs = betge_lucifer()
epochs.plot()

symmetry = "Neuroscans_OCD_metacognition/sub-044_task-symmetry.cnt"
epochs_sym = betge_symmetry(symmetry)
print(len(epochs_sym))


lucifer = "Neuroscans_OCD_metacognition/sub-042_task-lucifer.cnt"
epochs = betge_lucifer(lucifer)
print(len(epochs))
