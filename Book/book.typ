// Globals
#let date = datetime.today().display("[day].[month].[year]")  

#set text(lang: "he")

#set page(
  header: align(
    center + horizon,
    grid(
      columns: 3,
      column-gutter: 130pt,
      [מגיש: שחר רתם],
      [שם הפרויקט: Hive],
      [תאריך: #date]
    )
  ),
  numbering: "1/1",
  number-align: bottom + left
)

// Page 1

#align(center, [#image("assets/school_logo.png", width: 175pt)])
#align(center + horizon, 
  heading[
    כותר לפרויקט \
    (סלוגן)
  ]
) \ \ \ \ \ \ \

#align(
  horizon + right,
  heading[
    שם התלמיד: שחר רתם \
    מספר ת.ז: 215792490 \
    מורה: יהורם אביטוב \
    תאריך הגשה: #date
  ]
)

#pagebreak() \
// Page 2

#heading[
  #text(blue)[
    #underline[טבלת שינויים לאורך מימוש הפרויקט]
  ]
]

#table(
  columns: 4,

  rows: 6,
  [פעילות], [גרסה], [תכולה/שינוי], [תאריך סיום],
  [יזום], [0.1], [], [],
  [אפיון דרישות, \ ארכיטקטורת מערכת, \ כלי פיתוח], [0.2], [], [],
  [קידוד שלד עובד], [1.0], [], [],
  [קידוד], [2.0], [], [],
  [קידוד], [3.0], [], []
)

#pagebreak() \
// Page 3

