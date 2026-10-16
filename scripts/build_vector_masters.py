#!/usr/bin/env python3
"""Hand-authored, editable vector reconstruction of NAON2 (not pixel-identical source)."""
from pathlib import Path
import cairosvg

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'assets/masters/vector-v01'
OUT.mkdir(parents=True,exist_ok=True)

DEFS='''<defs>
<linearGradient id="fur" x1="0.18" y1="0" x2="0.88" y2="1" objectBoundingBox="true"><stop offset="0" stop-color="#9d7c76"/><stop offset="0.36" stop-color="#796164"/><stop offset="0.74" stop-color="#644c54"/><stop offset="1" stop-color="#493948"/></linearGradient>
<linearGradient id="bodyfur" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#816369"/><stop offset="0.65" stop-color="#604a53"/><stop offset="1" stop-color="#483945"/></linearGradient>
<linearGradient id="cream" x1="0" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#fff9f1"/><stop offset="0.63" stop-color="#fff1e8"/><stop offset="1" stop-color="#eed8d5"/></linearGradient>
<linearGradient id="ear" x1="0" y1="0" x2="0.85" y2="1"><stop offset="0" stop-color="#ffbbbf"/><stop offset="0.6" stop-color="#f783a0"/><stop offset="1" stop-color="#bd657f"/></linearGradient>
<linearGradient id="tail" x1="0.2" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#a67d6d"/><stop offset="0.53" stop-color="#72545a"/><stop offset="1" stop-color="#493a47"/></linearGradient>
<linearGradient id="tip" x1="0" y1="0" x2="0.85" y2="1"><stop offset="0" stop-color="#edba82"/><stop offset="0.55" stop-color="#cd8955"/><stop offset="1" stop-color="#996b55"/></linearGradient>
<linearGradient id="iris" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#120f1b"/><stop offset="0.53" stop-color="#2a1720"/><stop offset="0.78" stop-color="#73402e"/><stop offset="1" stop-color="#b46b36"/></linearGradient>
<radialGradient id="eyeWhite"><stop offset="0" stop-color="#ffffff"/><stop offset="0.77" stop-color="#fffdfa"/><stop offset="1" stop-color="#e3ced1"/></radialGradient>
<radialGradient id="muzzle"><stop offset="0" stop-color="#fffdf5"/><stop offset="0.7" stop-color="#fff5ec"/><stop offset="1" stop-color="#eddbd9"/></radialGradient>
<linearGradient id="pinks" x1="0.25" y1="0" x2="0.8" y2="1"><stop offset="0" stop-color="#ffb3ad"/><stop offset="1" stop-color="#e46a87"/></linearGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>
</defs>'''

# Hand-drawn path helpers. Views share the same gradients, outlines and shape language.
def p(path, fill, stroke='#543e48', sw=7, extra=''):
    return f'<path d="{path}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round" {extra}/>'
def ell(cx,cy,rx,ry,fill,stroke='#493741',sw=6,extra=''):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def cp(path,col='#e9d4d5',width=3,opacity='.68'):
    return f'<path d="{path}" fill="none" stroke="{col}" stroke-width="{width}" opacity="{opacity}" stroke-linecap="round"/>'
def circle(cx,cy,r,fill):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'

def front():
 a=[]
 # tails behind body, exactly as in approved 3-view: two fluffy lobes peeking out
 # One tail only (on the right). The approved concept sheet suggests two visible lobes, but a single anatomical tail is standardized here.
 a.append(p('M646 726 C751 777 868 736 864 626 C863 560 883 520 857 480 C836 450 802 457 789 477 C773 500 782 522 790 539 C803 562 832 560 835 530 C843 596 802 659 733 650 L657 615 Z','url(#tail)',sw=9))
 a.append(p('M789 477 C807 452 841 460 856 479 C867 496 870 525 863 561 C850 540 836 536 826 536 C820 509 795 513 782 522 C778 503 779 491 789 477 Z','url(#tip)','none',0))
 a.append(cp('M712 697 C778 702 823 655 835 608', '#bd9b92', 12, '.35'))
 # body and soft chest
 a.append(p('M382 598 C307 621 294 718 315 810 C337 878 432 907 504 902 C584 901 678 885 691 809 C704 724 678 629 620 605 C548 575 459 577 382 598 Z','url(#bodyfur)',sw=9))
 a.append(ell(365,775,85,93,'url(#bodyfur)',sw=8));a.append(ell(637,773,85,94,'url(#bodyfur)',sw=8))
 a.append(p('M447 626 Q485 650 500 646 Q526 648 557 620 C565 689 603 764 583 829 C567 882 536 894 499 898 C461 895 419 878 409 829 C397 766 439 689 447 626 Z','url(#cream)','none',0))
 a.append(p('M434 645 C426 720 417 760 425 796 M564 647 C572 710 588 765 574 809','none','#a48b8a',3,extra='opacity=".25"'))
 # feet, two front legs in front of torso
 for x,sgn in ((408,-1),(591,1)):
  a.append(p(f'M{x-45} 755 Q{x-57} 810 {x-44} 853 C{x-37} 890 {x+39} 901 {x+49} 858 L{x+35} 772 Q{x-7} 742 {x-45} 755 Z','url(#cream)',sw=7))
  a.append(p(f'M{x-46} 751 Q{x-13} 730 {x+19} 750 L{x+35} 785 Q{x+5} 765 {x-24} 782 Z','url(#fur)','none',0))
  for shift in (-19,2,22):a.append(cp(f'M{x+shift} 873 q-6 -13 -2 -20','#d79f9e',3,'.7'))
  a.append(ell(x-5,861,12,9,'url(#pinks)','none',0))
 a.append(ell(318,850,43,37,'url(#cream)',sw=6))
 a.append(ell(681,852,43,37,'url(#cream)',sw=6))
 for j,x in enumerate((305,327,672,692)):
  a.append(ell(x,863-(j%2)*6,11,7,'url(#pinks)','none',0))
 # ears behind face
 a.append(p('M291 332 C281 249 278 173 310 129 C330 111 401 165 440 231 L423 344 Z','url(#fur)',sw=10))
 a.append(p('M711 332 C720 249 724 173 689 129 C671 112 601 165 563 231 L577 344 Z','url(#fur)',sw=10))
 a.append(p('M302 308 C296 242 300 190 318 157 Q360 190 399 244 Q353 258 302 308Z','url(#ear)','#a36677',4))
 a.append(p('M700 308 C707 242 702 189 681 157 Q642 190 600 244 Q645 258 700 308Z','url(#ear)','#a36677',4))
 a.append(cp('M311 267 Q309 201 320 176 M687 266 Q695 210 683 178','#ffd3ce',8,'.6'))
 # big floofy head: round plus tufts 
 a.append(p('M501 245 C637 236 720 320 731 441 Q740 487 758 506 L742 518 L755 536 L733 547 C737 598 675 652 605 659 C548 675 457 674 395 659 C330 649 267 609 267 546 L248 535 L258 518 L241 506 Q258 481 268 437 C285 312 370 244 501 245 Z','url(#fur)',sw=10))
 # forehead soft patches and fur tufts
 a.append(p('M453 291 Q472 310 490 297 M553 294 Q536 313 520 298','none','#bc9c91',6,extra='opacity=".30"'))
 a.append(p('M463 326 C475 352 487 373 501 384 C508 369 516 348 525 329 C520 375 525 414 552 437 L499 494 L444 439 C474 411 468 376 463 326 Z','url(#cream)','none',0))
 # white mask cheeks joining under muzzle
 a.append(p('M368 480 C396 450 455 448 496 475 C550 446 611 451 648 481 C694 508 703 562 674 598 C633 654 549 657 504 660 C453 658 365 654 327 606 C297 568 317 514 368 480 Z','url(#muzzle)','none',0))
 a.append(ell(375,552,66,47,'#fff7ef','none',0,'opacity=".38"'))
 a.append(ell(628,552,66,47,'#fff7ef','none',0,'opacity=".38"'))
 # eyes, biggest identity anchors
 for x in (408,596):
  a.append(ell(x,435,67,80,'url(#eyeWhite)','#392f37',8))
  a.append(ell(x+5,441,45,60,'url(#iris)','#231e27',5))
  a.append(ell(x+9,424,32,40,'#11101a','none',0))
  a.append(ell(x-13,402,18,23,'#ffffff','none',0))
  a.append(circle(x+24,457,7,'#fffaf3'))
  a.append(cp(f'M{x-47} 399 C{x-35} 369 {x+9} 356 {x+43} 393','#f2dfdc',3,'.50'))
 # beige brows
 a.append(p('M381 345 Q400 325 415 345 Q416 360 397 364 Q380 361 381 345Z','#b49a95','none',0,'opacity=".8"'))
 a.append(p('M578 345 Q595 327 614 346 Q619 360 601 365 Q582 362 578 345Z','#b49a95','none',0,'opacity=".8"'))
 # chin face / nose
 a.append(p('M483 526 Q498 518 518 524 Q518 537 502 546 Q488 541 483 526 Z','url(#pinks)','#7b5059',4))
 a.append(cp('M500 545 L500 559','#805965',4, '1'))
 a.append(cp('M499 556 C486 577 460 578 450 563 M502 555 C515 576 538 579 550 558','#74505a',5,'1'))
 a.append(ell(428,556,22,11,'#ffabb6','none',0,'opacity=".13"'))
 a.append(ell(578,556,22,11,'#ffabb6','none',0,'opacity=".13"'))
 # whiskers clipped close to head, fine subtle strokes
 for s in (0,1):
  group=''
  for dy in (0,18,36): group+=cp(f'M345 {544+dy} Q298 {531+dy} 266 {539+dy}', '#d7bebc', 3,'.53')
  a.append(group if not s else f'<g transform="translate(1000 0) scale(-1 1)">{group}</g>')
 # highlights tuft cuts
 a.append(cp('M294 531 l-14 -7 M708 532 l14 -7', '#c8aea8', 4,'.5'))
 return ''.join(a)

def side():
 a=[]
 # tail behind body
 a.append(p('M652 734 C741 773 858 742 864 627 C874 531 843 491 799 490 C767 491 754 529 772 554 C780 566 809 568 827 545 C824 622 791 644 730 626 L660 609 Z','url(#tail)',sw=10))
 a.append(p('M785 490 C833 467 873 512 859 568 C845 547 822 532 807 549 C791 532 782 511 785 490 Z','url(#tip)','none',0))
 # body sideways, front pointed left
 a.append(p('M479 600 C582 578 674 628 701 737 C727 826 654 887 541 894 C432 899 394 835 413 752 C423 675 444 630 479 600 Z','url(#bodyfur)',sw=9))
 a.append(p('M440 645 Q465 612 513 628 C475 677 482 785 490 860 Q430 871 411 813 C397 737 420 677 440 645Z','url(#cream)','none',0))
 a.append(ell(623,799,79,95,'url(#bodyfur)',sw=8))
 a.append(ell(617,870,81,27,'url(#cream)',sw=6))
 a.append(ell(450,861,65,29,'url(#cream)',sw=6))
 for xx in (409,429,447):a.append(cp(f'M{xx} 867 l-3 -13','#ca9c9e',4,'.65'))
 # back ear subdued
 a.append(p('M528 319 Q550 203 612 148 Q643 212 632 319 Z','url(#bodyfur)',sw=8))
 a.append(p('M558 284 L608 177 Q622 222 619 281 Z','url(#ear)','none',0))
 # front ear
 a.append(p('M336 333 Q305 225 356 132 Q415 138 460 281Z','url(#fur)',sw=10))
 a.append(p('M348 291 Q330 227 361 163 Q402 184 428 266 Z','url(#ear)','#a96e79',4))
 # head silhouette, projecting muzzle left side
 a.append(p('M480 258 C617 248 687 332 689 440 C697 505 662 583 617 619 C564 655 470 657 416 625 C372 609 338 585 333 551 C307 544 293 532 295 509 C298 489 324 477 331 456 C330 340 382 270 480 258 Z','url(#fur)',sw=10))
 a.append(p('M361 437 C385 398 405 356 413 345 C410 398 432 433 459 451 L413 499 L343 487 Q335 457 361 437Z','url(#cream)','none',0))
 # white muzzle shape following left-facing mouth
 a.append(p('M348 472 Q375 462 426 477 C475 454 532 462 572 494 C606 527 616 590 572 621 C530 654 460 634 411 619 Q359 601 339 563 C315 557 302 547 298 527 C291 503 310 488 348 472 Z','url(#muzzle)','none',0))
 # large near eye oval at left, keep warm iris brown
 a.append(ell(426,448,68,86,'url(#eyeWhite)','#3c3036',9))
 a.append(ell(412,453,48,65,'url(#iris)','#28202a',5))
 a.append(ell(410,435,35,44,'#0d1019','none',0))
 a.append(ell(397,416,19,24,'white','none',0));a.append(circle(432,467,8,'#ffffff'))
 # little pink profile nose and mouth
 a.append(p('M297 514 Q311 503 323 509 Q319 525 304 529 Z','url(#pinks)','#684854',4))
 a.append(cp('M307 528 Q324 554 347 537','#76505d',5,'1'))
 a.append(ell(368,557,16,9,'#f8b3ad','none',0,'opacity=".3"'))
 a.append(p('M452 354 q8 -20 26 -6','none','#bca09d',8,extra='opacity=".55"'))
 a.append(cp('M338 531 Q301 519 274 531 M341 545 Q309 541 282 558', '#cfb6b5',3,'.6'))
 return ''.join(a)

def back():
 a=[]
 # visible curved tail waving right
 a.append(p('M640 726 C720 770 832 738 865 670 C897 606 890 515 839 484 C789 459 750 496 755 533 C757 565 789 587 815 562 C819 609 772 646 689 618 L628 600 Z','url(#tail)',sw=10))
 a.append(p('M834 483 C872 492 898 537 885 598 C862 571 851 546 813 555 C792 551 781 519 799 492 C810 481 824 481 834 483 Z','url(#tip)','none',0))
 a.append(cp('M711 703 Q787 725 842 649','#b99588',12,'.29'))
 # body
 a.append(p('M387 596 C321 640 303 727 320 808 Q339 885 488 892 Q631 900 688 816 C714 720 673 627 614 599 Z','url(#bodyfur)',sw=9))
 a.append(cp('M364 718 Q332 785 362 836 M640 725 Q683 797 646 841','#aa8990',12,'.26'))
 a.append(ell(388,843,75,50,'url(#bodyfur)',sw=8))
 a.append(ell(618,843,73,50,'url(#bodyfur)',sw=8))
 a.append(ell(408,874,50,23,'url(#cream)',sw=6));a.append(ell(612,876,49,23,'url(#cream)',sw=6))
 # ears
 a.append(p('M307 318 C286 240 293 171 326 140 C361 144 410 194 440 258 Z','url(#fur)',sw=9))
 a.append(p('M699 318 C716 243 709 169 679 140 C639 148 596 194 563 257 Z','url(#fur)',sw=9))
 a.append(cp('M312 268 Q309 198 327 159 M692 269 Q698 201 680 161','#b18d8a',8,'.4'))
 # rear head
 a.append(p('M503 239 C636 242 726 325 731 439 L752 505 L735 522 L746 537 L726 545 C733 594 675 645 605 662 C547 678 460 678 394 657 C328 641 271 600 273 542 L257 532 L268 516 L248 504 C259 440 276 326 380 268 Q437 238 503 239 Z','url(#fur)',sw=10))
 a.append(cp('M371 300 C418 268 451 259 494 255 M624 308 C590 277 558 258 529 254','#cfaaa0',8,'.20'))
 a.append(p('M500 242 Q505 254 505 273','none','#bea09a',5,extra='opacity=".4"'))
 # rear lower white butt partially above paws
 a.append(p('M477 837 Q503 816 535 839 C559 859 557 891 517 893 Q471 894 464 864Z','url(#cream)','none',0))
 a.append(cp('M379 611 Q339 600 306 549 M620 614 Q667 602 698 552','#b59c9c',5,'.25'))
 return ''.join(a)

for name,creator in (('front',front),('side',side),('back',back)):
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="2048" height="2048" viewBox="0 0 1000 1000">{DEFS}<g>{creator()}</g></svg>'
    (OUT/f'naon2-{name}-vector-master-v01.svg').write_text(svg,encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(OUT/f'naon2-{name}-vector-master-v01.png'),output_width=2048,output_height=2048)
    print(name,len(svg), (OUT/f'naon2-{name}-vector-master-v01.png').stat().st_size)