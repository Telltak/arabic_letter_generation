#import "@preview/suiji:0.4.0": *
#set text(lang: "ar")

#{
  let question_count_seed = gen-rng-f(int(sys.inputs.at("count_seed", default: 1000)))
  let question_length_seed = gen-rng-f(int(sys.inputs.at("length_seed", default: 1000)))
  let (_, question_seeds) = integers-f(
    question_count_seed,
    low: 1,
    high: 2147483648,
    size: int(sys.inputs.at("questions", default: 10)),
  )
  let (_, question_lengths) = integers-f(
    question_length_seed,
    low: 2,
    high: int(sys.inputs.at("question_length", default: 5)),
    size: question_seeds.len(),
  )
  for (i, v) in question_seeds.enumerate() {
    [#int(i + 1):#h(2%)]
    let rng = gen-rng-f(v)
    let (_, chars) = integers-f(rng, low: 1575, high: 1609, size: question_lengths.at(i))
    for (ci, cv) in chars.enumerate() {
      if cv == 1600 {
        cv += 1
      }
      [#str.from-unicode(cv)]
      if ci != chars.len() - 1 {
        [#h(1%),#h(1%)]
      }
    }
    [#h(2%)=#line(length: 100%)\ ]
  }
}

