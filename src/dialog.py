# A python file for storing dialog prompts and whatnot.
# This helps to keep the main files less cluttered
# and easier to navigate.


# Set a couple of containers so its easy to see
# what each section of text is for.
# Fx. main.calmissing prints on main() when
# there is no calendar open.
# and cal.open prints when on the calendar file open
# prompt.
class Container():
    pass

main = Container
cal = Container

setattr(main, "intro", [
    "Osocomp; En simpelt kalendar.",
])

setattr(main, "calmissing", [
        "\n- - - - - - - -",
        "\nDu har ikke åbnet en",
        "\nkalendar fil endnu.",
        "\ntast \"o\" til at åbne",
        "\nmenuen",
        "\n- - - - - - - -"
])

setattr(main, "basichelp", [
    "\nTast \"o\" for at åbne et kalendar.",
    "\nTast \"q\" for at lukke programmet.",
    "\nTast \"h\" for hjælp til at bruge programmet.",
    "\nTast \"i\" for mere information om programmet.",
    "\nTast \"c\" for ophavsret information.\n"
])

setattr(cal, "open", [
    "Vær sød at skrive filnavnen af kalendaren som",
    "\nDu vil gerne åben ellers så kan du ",
    "\nSkriv \"quit\" for at lukke programmet."
])

info = [
    "osocomp -- Abdul's tredje OSO produkt",
    "\n",
    "\n\tHvad er det her?",
    "\nDet her er Abdul's tredje OSO produkt. Produktet er et slags program,",
    "\nder tjekker ens kalendar for én og forudser vejret til når man skal",
    "\nudenfor, så hvis man nu skal til en fest, så viser den, hvordan vejret",
    "\nbliver fra når man er ude til, at man kommer hjem igen. Den siger så",
    "\nnoget om, hvis man skal tage jakke på eller hvad end der passer til",
    "\nvejret.",
    "\n",
    "\n\tHvorfor er dette program tekst-baseret?",
    "\nDet er umuligt at lave et program med alle disse funktioner på en uge,",
    "\nnår man arbejder med grafiske programmer. Det er også vigtigt, at",
    "\ndette program virker på alle slags systemer, da forskellige systemer",
    "\nhar forskellige \"grafisk værktøjsset\" (altså de programmer som gør",
    "\ndet muligt for programmer at lave grafiske vinduer), Windows har deres",
    "\negen som kaldes for \"WinUI\", MacOS har \"UIKit\", HaikuOS har",
    "\n\"Interface Kit\", og Linux har \"xlib\" men de fleste",
    "\nsoftwareudviklere bruger \"GTK\" eller \"Qt\". Det er ikke umuligt at",
    "\nlave et grafisk program, som virker på alle disse systemer men det er",
    "\nvirkelig svært og det tager sin tid.",
    "\n",
    "\n\tHvem har skrevet dette program?",
    "\nDet har jeg, Abdul Karim Kikar. Jeg begyndte med at skrive dette",
    "\nprogram i december 2022, lidt før før OSO-ugen fordi jeg på forhånd",
    "\nvidste, at det ville være ufattelig svært at få lavet 3 produkter på",
    "\nkun en uge, og samtidig også gøre alle andre ting klar (fremlæggelse,",
    "\ninterview osv.) Dette program er licenseret under GNU GPL version 3",
    "\neller også på nyere versioner. Du kan få kildekoden ved selv at spørge",
    "\nAbdul (mig).",
    "\n",
    "\nMange tak til Halima, hun har rettede denne besked!"
]
