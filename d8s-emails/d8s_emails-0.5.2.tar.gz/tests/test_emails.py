from d8s_emails import (
    is_email,
    email_header_date_fix,
    email_read,
    email_object_new,
    email_content_transfer_encoding,
    email_bodies_as_strings,
    email_bodies_as_objects,
    email_attachments,
    email_attachments_objects,
    email_body_is_base64,
    email_header_fields,
    email_headers,
    email_headers_raw,
    email_headers_as_dict,
    email_header,
    email_header_delete_field,
    email_structure,
    email_header_add_raw,
    email_header_add,
)
from d8s_emails.emails import _email_structure_iterator, _is_email_object

SIMPLE_EMAIL_TEXT = """Subject: Buy bitcoin now!
From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi!"""

LONG_EMAIL = """Delivered-To: REDACTED\r\nReceived: by 2002:a4a:3503:0:0:0:0:0 with SMTP id l3csp860305ooa;\r\n        Sat, 17 Nov 2018 11:36:28 -0800 (PST)\r\nX-Google-Smtp-Source: AJdET5eeftbIotu4JyQiSyZ2JzspoTeNMxFAQKMnur4oIWNzI6lpzxTYbgffo+iBkRIsXx0c51HN\r\nX-Received: by 2002:a25:1009:: with SMTP id 9-v6mr14807713ybq.487.1542483388508;\r\n        Sat, 17 Nov 2018 11:36:28 -0800 (PST)\r\nARC-Seal: i=1; a=rsa-sha256; t=1542483388; cv=none;\r\n        d=google.com; s=arc-20160816;\r\n        b=aw/5FwBfmm5NmVnVGGCg3eduYB6zwYvWzbnO31yxoKEezcdh93DgPIJyt1I3zE17Ok\r\n         h2EHCRSZe67pb7M4HaDrhaMSeTSYU9qwfNOnIse+6XU7oX/k8oG/R6066RyTYhHO6IRD\r\n         54/XMuaWTJYyigAmUcrba+UNo4Kg0CFhkE1KF8QiDwGUIZj69D3bNurBcz7kpYYQd7nl\r\n         Tif3yim3TDglf8ctOPQSRIQr/NAVtR7CtjTfm+GOjfe+F3vS+t3b/68GXbsLnnG3W5wB\r\n         iisKId1dFpU4A1O/9RkIBYBjoZBgmgxBBUl8ChT5I5fwpNBZ8lA1wuqhOA5MH0ltcE5W\r\n         Ou7g==\r\nARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=google.com; s=arc-20160816;\r\n        h=to:subject:mime-version:message-id:list-unsubscribe:from:date\r\n         :dkim-signature;\r\n        bh=DHO8A0EaUQt3zaV8QwGdmjRumZs0we9+DIeFteG47K4=;\r\n        b=ib/ZotE8wDVanoJP9AvxCQjYhr/K4/uA9dR2XOjzXGDnRpcnJYWt+EO90+/kFCTcpA\r\n         YwogHFe0R0c1YP2gX6pQ0TGNDce8Eg9OZ7e08aU/vONOl2lJi/uffRfogvsX2wyPtfH3\r\n         U5neMwlEX3Au+X4ocQr8OeqC0l/zj7Vg06baXcaGC7mebOIyUrapYAaTUGtd8Q0RrjFT\r\n         Sw7Nf554vBxh8Jef9gWgXoVGSGxoMKmPrypLmRWD96JS8v6/fkYJRm9n3p7RDDEu6ls3\r\n         CInvWhJAXQ3eiR76S5Be7v+19FdNTdQ3cM1wWN4T4XIl08OqXszmUgyAn2IYkiNzEQ16\r\n         //TQ==\r\nARC-Authentication-Results: i=1; mx.google.com;\r\n       dkim=pass header.i=@mapbox.com header.s=smtpapi header.b=TbRWHoCf;\r\n       spf=pass (google.com: domain of bounces+866407-b8b0-REDACTED=REDACTED@delivery.customeriomail.com designates 167.89.43.193 as permitted sender) smtp.mailfrom=\"bounces+866407-b8b0-REDACTED=REDACTED@delivery.customeriomail.com\";\r\n       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=mapbox.com\r\nReturn-Path: <bounces+866407-b8b0-REDACTED=REDACTED@delivery.customeriomail.com>\r\nReceived: from o32.delivery.customeriomail.com (o32.delivery.customeriomail.com. [167.89.43.193])\r\n        by mx.google.com with ESMTPS id j184-v6si19384010ywc.173.2018.11.17.11.36.27\r\n        for <REDACTED>\r\n        (version=TLS1_2 cipher=ECDHE-RSA-AES128-GCM-SHA256 bits=128/128);\r\n        Sat, 17 Nov 2018 11:36:28 -0800 (PST)\r\nReceived-SPF: pass (google.com: domain of bounces+866407-b8b0-REDACTED=REDACTED@delivery.customeriomail.com designates 167.89.43.193 as permitted sender) client-ip=167.89.43.193;\r\nAuthentication-Results: mx.google.com;\r\n       dkim=pass header.i=@mapbox.com header.s=smtpapi header.b=TbRWHoCf;\r\n       spf=pass (google.com: domain of bounces+866407-b8b0-REDACTED=REDACTED@delivery.customeriomail.com designates 167.89.43.193 as permitted sender) smtp.mailfrom=\"bounces+866407-b8b0-REDACTED=REDACTED@delivery.customeriomail.com\";\r\n       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=mapbox.com\r\nDKIM-Signature: v=1; a=rsa-sha1; c=relaxed/relaxed; d=mapbox.com; \r\n\th=content-type:from:list-unsubscribe:mime-version:subject:to; \r\n\ts=smtpapi; bh=SEWKRTmEJ7oQrNXDRgyRpVNc4ug=; b=TbRWHoCfVD4qV9DiQc\r\n\tkHEY0Jq6ltNf1q0JLc00R62QWYmZ4/GJ0tk9huO2xjtialGKl6xh692i+RRHn5M7\r\n\t5bZIv5id7mlviXsPg5u+plbFlKSGN6Kcozw0LR0ajHFABQKduiFXgP93cwxjWVCu\r\n\tvwR4qCgFM52/NQ6Y7P6dE/Ag0=\r\nReceived: by filter0340p1iad2.sendgrid.net with SMTP id filter0340p1iad2-11127-5BF06DBA-9\r\n        2018-11-17 19:36:26.615921922 +0000 UTC m=+156187.835508479\r\nReceived: from localhost (6.worker.customeriomail.com [104.154.144.51])\r\n\tby ismtpd0025p1iad2.sendgrid.net (SG) with ESMTP id I60jc0QFRN-1LDRjia7mIQ\r\n\tfor <REDACTED>; Sat, 17 Nov 2018 19:36:26.866 +0000 (UTC)\r\nContent-Type: multipart/alternative; boundary=\"4ec723ec450348fac2a3f736f3164140329c965382c7f43303f327961078\"; charset=\"utf-8\"\r\nDate: Sat, 17 Nov 2018 19:36:26 +0000 (UTC)\r\nFrom: \"Eric Gundersen\" <newsletter@mapbox.com>\r\nList-Unsubscribe: <mailto:32.LJGXG3KBIFDG4SLZPFSDIVTTJY3WGNRWINEXS52YMNKT2===@unsubscribe2.customer.io>, <http://email.mapbox.com/unsubscribe/ZMsmAAFnIyyd4VsN7c66CIywXcU=>\r\nMessage-Id: <ZMsmAAFnIyyd4VsN7c66CIywXcU.1542483386@mapbox.com>\r\nMime-Version: 1.0\r\nSubject: Scary maps\r\nTo: <REDACTED>\r\nX-Mailer: Customer.io (ZMsmAAFnIyyd4VsN7c66CIywXcU=; +https://whatis.customeriomail.com)\r\nX-Report-Abuse-To: badactor@customer.io\r\nX-SG-EID: Y7YmidTofRIcIU+Tt5NvcofUpkZMkM+JruComX1+N3WAvnjXueITA0OpKGbmFP2AZpbGz1GPNO16tu\r\n QGQ95PJpYhBOpgnBwR37qKcxPxM1sNPrGRZgFOn/JO2iaJ80I3GBUKASH/Q9gxa0YukOAFob7ZozA9\r\n v2eWRxxOY3klrB/84aIv4hwLde9taXldLy9daQEgDkdlhn/1+9trg9vmNnl9X7LeFW1exvE9+KbiEd\r\n U=\r\nX-SG-ID: YDTqBOjidbCUo/ar1oAtZj/K/mwVckVWZmEAcL448dd59/NNA/K8iQ5NGb2cbAeRcsPO23F3Cs5IL9\r\n 7VU5vYCw==\r\n\r\n--4ec723ec450348fac2a3f736f3164140329c965382c7f43303f327961078\r\nContent-Id: text/plain.ZMsmAAFnIyyd4VsN7c66CIywXcU.1542483386@mapbox.com\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/plain; charset=\"utf-8\"\r\nDate: Sat, 17 Nov 2018 19:36:26 +0000\r\nMime-Version: 1.0\r\n\r\nWhen you=E2=80=99re heading in the wrong direction, your map should tell yo=\r\nu. I just landed home at SFO, sunrise was a thick haze with the smoke from =\r\nthe Camp Fire still burning up in Butte County. Today, maps are a giving us=\r\n a warning. Showing not just where we are now, but the future we are headin=\r\ng toward. When we=E2=80=99re warned to the hazards on the road ahead, we ha=\r\nve a chance to reroute in a different direction.\r\n\r\nThe air quality here is the worst in the world right now. Over breakfast, I=\r\n convinced my boys that N95 masks were cool. I ordered them before I left, =\r\nwhen the fires started. I=E2=80=99m lucky; the backlog on Amazon is now two=\r\n weeks. Should have ordered them last year after the big fires in October b=\r\nut didn=E2=80=99t. This is starting to feel like a pattern.\r\n\r\nEveryone is rubbing their eyes. The air is dry. Everything=E2=80=99s dry. C=\r\nalifornia is as dry as it=E2=80=99s ever been this time of year. Up until l=\r\nast week, temperatures in the Bay Area were hitting the mid-70s every day. =\r\nThe forecast is finally calling for rain the day before Thanksgiving.\r\n\r\nThis data is dense. While hard to understand what, say, emissions data mean=\r\ns, there=E2=80=99s something visceral about actually visualizing it. Or in =\r\nthe case of most of us in California today, just breathing and feeling it i=\r\nn our lungs.\r\n\r\n( https://blog.mapbox.com/scary-maps-a-warning-9bb4ab7254b8 )\r\n\r\nWe have to stop this. We need look at the data to understand how to solve t=\r\nhis at the root. The UN says that our ability to substantially bring down e=\r\nmissions by 2030 will determine if an Alaska-sized area of arctic permafros=\r\nt will melt (read: a lot more carbon in the atmosphere) or stay frozen. Tod=\r\nay atmospheric CO2 is at 407 parts per million. That=E2=80=99s up almost 30=\r\n% from 1960, when it was 320. Atmospheric methane (CH4)=E2=80=94which dissi=\r\npates much faster than CO2, over a decade or two, but in that time traps ab=\r\nout 70x more heat=E2=80=94has a concentration of about 1850 parts per billi=\r\non today. That=E2=80=99s up from 1650 ppb in 1985. What does that actually =\r\nlook like?\r\n\r\nThis map from Bread For The World is striking ( https://medium.com/maptian/=\r\nvisualizing-near-surface-air-temperature-in-2100-d38816d61ad9 ), visualizin=\r\ng 12TB data set of global temperature data for 1950, today, and 2100=E2=80=\r\n=94assuming we maintain this killer pace of inaction=E2=80=94for everywhere=\r\n in the world, broken into a million different points. An average global te=\r\nmperature rise of 8.5=C2=B0C (about 15=C2=B0F) means it=E2=80=99ll be routi=\r\nnely hitting 122=C2=B0F in Saudi Arabia, and 110=C2=B0F in Texas by 2100. T=\r\no be honest that feels low, but the map and data is quite dramatic.\r\n\r\nIt was amazing working this week with BuzzFeed, Zillow, and Climate Central=\r\n to visualize sea level rise and flood risk for 385,000 US homes ( https://=\r\nwww.buzzfeednews.com/article/zahrahirji/climate-change-map-homes-flooding )=\r\n that will be in routine flood zones by 2050, about the time when today=E2=\r\n=80=99s home buyers will just finish paying off their home mortgage. It=E2=\r\n=80=99s shocking to consider the amount of building that=E2=80=99s still go=\r\ning on in the highest risk areas. Since 2009, New Jersey has added 2,700 ne=\r\nw homes in high-risk areas, currently worth about $2.6 billion. We=E2=80=99=\r\nve also been playing with different styles and data layers ( https://www.ma=\r\npbox.com/narratives/active-fires/#3/42.99/-97.67 ) on a fire map, to track =\r\nall the\r\nblazes in California and elsewhere. It=E2=80=99s scary.\r\n\r\nIf we want to make progress, science, data, and truth have to matter. Peopl=\r\ne have to care, and for that they have to understand. I=E2=80=99m hopeful t=\r\nhat maps can be part of telling a story in a way that resonates, that by vi=\r\nsualizing a future we don=E2=80=99t want, we can find our way to a safer on=\r\ne. Let=E2=80=99s keep building for something better.\r\n\r\n=E2=80=94 Eric\r\n\r\nView this post on Medium ( https://blog.mapbox.com/scary-maps-a-warning-9bb=\r\n4ab7254b8 )\r\n\r\n-------\r\n\r\nDon't want to receive this type of email from us?\r\nUnsubscribe ( http://track.customer.io/unsubscribe/ZMsmAAFnIyyd4VsN7c66CIyw=\r\nXcU=3D )\r\n\r\n740 15th St NW, Suite 500, Washington, DC 20005=\r\n\r\n--4ec723ec450348fac2a3f736f3164140329c965382c7f43303f327961078\r\nContent-Id: text/html.ZMsmAAFnIyyd4VsN7c66CIywXcU.1542483386@mapbox.com\r\nContent-Transfer-Encoding: quoted-printable\r\nContent-Type: text/html; charset=\"utf-8\"\r\nDate: Sat, 17 Nov 2018 19:36:26 +0000\r\nMime-Version: 1.0\r\n\r\n<!DOCTYPE html PUBLIC \"-//W3C//DTD HTML 4.0 Transitional//EN\" \"http://www.w=\r\n3.org/TR/REC-html40/loose.dtd\"><html><head>\r\n<meta http-equiv=3D\"Content-Type\" content=3D\"text/html; charset=3DUTF-8\"/>\r\n    <style type=3D\"text/css\">\r\n      body { margin:10; padding: 0; font-family: sans-serif; font-size:13px=\r\n; font-style: normal;}\r\n      h1 { font-size: 16px; line-height:20px; }\r\n      h2 { font-size: 14px; line-height:18px; }\r\n      p { font-size: 13px; line-height: 16px; }\r\n      .center { text-align: center }\r\n      .unsubscribe,\r\n      .address { color:#727272; line-height:18px; font-size: 11px; }\r\n      .unsubscribe a { color: #333 }\r\n\r\n      @media only screen and (max-device-width: 480px) {\r\n        body { width: 320px !important; margin: 0; padding: 0; }\r\n        td img { height:auto !important; max-width:100% !important;}\r\n      }\r\n    </style>\r\n\r\n  </head>\r\n<body style=3D\"font-family: sans-serif; font-size: 13px; font-style: normal=\r\n; margin: 10; padding: 0;\">\r\n    <!-- We'll replace this content tag with whatever you write in your ema=\r\nil  -->\r\n        <p style=3D\"font-size: 13px; line-height: 16px;\">\r\n        When you=E2=80=99re heading in the wrong direction, your map should=\r\n tell you. I just landed home at SFO, sunrise was a thick haze with the smo=\r\nke from the Camp Fire still burning up in Butte County. Today, maps are a g=\r\niving us a warning. Showing not just where we are now, but the future we ar=\r\ne heading toward. When we=E2=80=99re warned to the hazards on the road ahea=\r\nd, we have a chance to reroute in a different direction.\r\n</p>\r\n<p style=3D\"font-size: 13px; line-height: 16px;\">\r\nThe air quality here is the worst in the world right now. Over breakfast, I=\r\n convinced my boys that N95 masks were cool. I ordered them before I left, =\r\nwhen the fires started. I=E2=80=99m lucky; the backlog on Amazon is now two=\r\n weeks. Should have ordered them last year after the big fires in October b=\r\nut didn=E2=80=99t. This is starting to feel like a pattern.\r\n</p>\r\n<p style=3D\"font-size: 13px; line-height: 16px;\">\r\nEveryone is rubbing their eyes. The air is dry. Everything=E2=80=99s dry. C=\r\nalifornia is as dry as it=E2=80=99s ever been this time of year. Up until l=\r\nast week, temperatures in the Bay Area were hitting the mid-70s every day. =\r\nThe forecast is finally calling for rain the day before Thanksgiving.\r\n</p>\r\n<p style=3D\"font-size: 13px; line-height: 16px;\">\r\nThis data is dense. While hard to understand what, say, emissions data mean=\r\ns, there=E2=80=99s something visceral about actually visualizing it. Or in =\r\nthe case of most of us in California today, just breathing and feeling it i=\r\nn our lungs.\r\n    </p>\r\n=20=20=20=20\r\n=20=20=20\r\n    <br/>\r\n    <div class=3D\"align-center\">\r\n        <a href=3D\"http://email.mapbox.com/e/c/eyJlbWFpbF9pZCI6IlpNc21BQUZu=\r\nSXl5ZDRWc043YzY2Q0l5d1hjVT0iLCJocmVmIjoiaHR0cHM6Ly9ibG9nLm1hcGJveC5jb20vc2N=\r\nhcnktbWFwcy1hLXdhcm5pbmctOWJiNGFiNzI1NGI4IiwibGlua19pZCI6MTE1NzA4NDUyLCJwb3=\r\nNpdGlvbiI6MH0/22f8be40b2a98cd07d5c232a9f81159cfda13439880699583d31a00a23673=\r\n162\"><img src=3D\"https://farm5.staticflickr.com/4832/45876702062_ab6bbaa4f3=\r\n_b.jpg\"/></a>\r\n    </div>\r\n    <br/>\r\n=20=20=20=20\r\n    <p style=3D\"font-size: 13px; line-height: 16px;\">We have to stop this. =\r\nWe need look at the data to understand how to solve this at the root. The U=\r\nN says that our ability to substantially bring down emissions by 2030 will =\r\ndetermine if an Alaska-sized area of arctic permafrost will melt (read: a l=\r\not more carbon in the atmosphere) or stay frozen. Today atmospheric CO2 is =\r\nat 407 parts per million. That=E2=80=99s up almost 30% from 1960, when it w=\r\nas 320. Atmospheric methane (CH4)=E2=80=94which dissipates much faster than=\r\n CO2, over a decade or two, but in that time traps about 70x more heat=E2=\r\n=80=94has a concentration of about 1850 parts per billion today. That=E2=80=\r\n=99s up from 1650 ppb in 1985. What does that actually look like?\r\n</p>\r\n<p style=3D\"font-size: 13px; line-height: 16px;\">\r\n<a href=3D\"http://email.mapbox.com/e/c/eyJlbWFpbF9pZCI6IlpNc21BQUZuSXl5ZDRW=\r\nc043YzY2Q0l5d1hjVT0iLCJocmVmIjoiaHR0cHM6Ly9tZWRpdW0uY29tL21hcHRpYW4vdmlzdWF=\r\nsaXppbmctbmVhci1zdXJmYWNlLWFpci10ZW1wZXJhdHVyZS1pbi0yMTAwLWQzODgxNmQ2MWFkOS=\r\nIsImxpbmtfaWQiOjExNTcwODQ1MywicG9zaXRpb24iOjF9/66282af158282ac0c539fd2467cc=\r\nbe49c95bf5cf275694aed0f8288d1d376968\">This map from Bread For The World is =\r\nstriking</a>, visualizing 12TB data set of global temperature data for 1950=\r\n, today, and 2100=E2=80=94assuming we maintain this killer pace of inaction=\r\n=E2=80=94for everywhere in the world, broken into a million different point=\r\ns. An average global temperature rise of 8.5=C2=B0C (about 15=C2=B0F) means=\r\n it=E2=80=99ll be routinely hitting 122=C2=B0F in Saudi Arabia, and 110=C2=\r\n=B0F in Texas by 2100. To be honest that feels low, but the map and data is=\r\n quite dramatic.\r\n</p>\r\n<p style=3D\"font-size: 13px; line-height: 16px;\">\r\nIt was amazing working this week with BuzzFeed, Zillow, and Climate Central=\r\n to <a href=3D\"http://email.mapbox.com/e/c/eyJlbWFpbF9pZCI6IlpNc21BQUZuSXl5=\r\nZDRWc043YzY2Q0l5d1hjVT0iLCJocmVmIjoiaHR0cHM6Ly93d3cuYnV6emZlZWRuZXdzLmNvbS9=\r\nhcnRpY2xlL3phaHJhaGlyamkvY2xpbWF0ZS1jaGFuZ2UtbWFwLWhvbWVzLWZsb29kaW5nIiwibG=\r\nlua19pZCI6MTE1NzA4NDU0LCJwb3NpdGlvbiI6Mn0/3e53c2f07701197bf0669b5a3ee85b4bf=\r\n2a945e9d9bb2dc13a909e4fd329f2a7\">visualize sea level rise and flood risk fo=\r\nr 385,000 US homes</a> that will be in routine flood zones by 2050, about t=\r\nhe time when today=E2=80=99s home buyers will just finish paying off their =\r\nhome mortgage. It=E2=80=99s shocking to consider the amount of building tha=\r\nt=E2=80=99s still going on in the highest risk areas. Since 2009, New Jerse=\r\ny has added 2,700 new homes in high-risk areas, currently worth about $2.6 =\r\nbillion. We=E2=80=99ve also been playing with <a href=3D\"http://email.mapbo=\r\nx.com/e/c/eyJlbWFpbF9pZCI6IlpNc21BQUZuSXl5ZDRWc043YzY2Q0l5d1hjVT0iLCJocmVmI=\r\njoiaHR0cHM6Ly93d3cubWFwYm94LmNvbS9uYXJyYXRpdmVzL2FjdGl2ZS1maXJlcy8jMy80Mi45=\r\nOS8tOTcuNjciLCJsaW5rX2lkIjoxMTU3MDg0NTUsInBvc2l0aW9uIjozfQ/8ee6c2a98a7ef762=\r\n9763d98328beebc273d26a089d9d34d6b4f53831b834fed1\">different styles and data=\r\n layers</a> on a fire map, to track all the\r\n blazes in California and elsewhere. It=E2=80=99s scary.\r\n</p>\r\n<p style=3D\"font-size: 13px; line-height: 16px;\">\r\nIf we want to make progress, science, data, and truth have to matter. Peopl=\r\ne have to care, and for that they have to understand. I=E2=80=99m hopeful t=\r\nhat maps can be part of telling a story in a way that resonates, that by vi=\r\nsualizing a future we don=E2=80=99t want, we can find our way to a safer on=\r\ne. Let=E2=80=99s keep building for something better.</p>\r\n=20\r\n    <p style=3D\"font-size: 13px; line-height: 16px;\">=E2=80=94 Eric</p>\r\n  <div class=3D\"align-center\">\r\n  <p style=3D\"font-size: 13px; line-height: 16px;\"><em><a href=3D\"http://em=\r\nail.mapbox.com/e/c/eyJlbWFpbF9pZCI6IlpNc21BQUZuSXl5ZDRWc043YzY2Q0l5d1hjVT0i=\r\nLCJocmVmIjoiaHR0cHM6Ly9ibG9nLm1hcGJveC5jb20vc2NhcnktbWFwcy1hLXdhcm5pbmctOWJ=\r\niNGFiNzI1NGI4IiwibGlua19pZCI6MTE1NzA4NDUyLCJwb3NpdGlvbiI6NH0/47d7c2649c369b=\r\nacf6df0e3a3ab7bc76b94266241dad93eac5bf1bf207c066f4\">View this post on Mediu=\r\nm</a></em></p>\r\n</div>\r\n    <p class=3D\"unsubscribe\" style=3D\"font-size: 11px; line-height: 18px; c=\r\nolor: #727272;\">-------<br/>\r\n      Don&#39;t want to receive this type of email from us?\r\n      <a href=3D\"http://email.mapbox.com/unsubscribe/ZMsmAAFnIyyd4VsN7c66CI=\r\nywXcU=3D\" class=3D\"untracked\" style=3D\"color: #333;\">Unsubscribe</a><br/>\r\n      740 15th St NW, Suite 500, Washington, DC 20005</p>\r\n=20=20\r\n\r\n<img src=3D\"http://email.mapbox.com/e/o/eyJlbWFpbF9pZCI6IlpNc21BQUZuSXl5ZDR=\r\nWc043YzY2Q0l5d1hjVT0ifQ=3D=3D\" style=3D\"height: 1px !important; max-height:=\r\n 1px !important; max-width: 1px !important; width: 1px !important\"/></body>=\r\n</html>=\r\n\r\n--4ec723ec450348fac2a3f736f3164140329c965382c7f43303f327961078--\r\n\r\n.\r\n"""


def test_is_email_docs_1():
    assert not is_email('foo bar')
    assert not is_email('foo bar - this is definitely not an email!')
    assert is_email(SIMPLE_EMAIL_TEXT)

    # this is the text for an email, but should not be detected as an email b/c the header is not properly formatted and, therefore, if this text is parsed as an email, it will not have a body
    s = """From: AliceTo: BobSubject: FooBarDear Bob, Hi!"""
    assert not is_email(s)

    assert not is_email(1)


def test_email_header_date_fix_docs_1():
    s = '''Message-Id: <199901120345.LAA09379@www.textiles.org.tw>
Date: 1/11/99 11:28:24 AM Pacific Daylight Time
Reply-To: freedomnow@newmail.net'''
    results = email_header_date_fix(s)
    assert results == ['1/11/99 11:28:24 AM Pacific Daylight Time']


# def test_email_reformat_docs_1():
#     assert email_reformat(email_text) == 'fill'


# def test_email_fix_docs_1():
#     assert email_fix(email_text: str) == 'fill'


def test_email_read_docs_1():
    email_object = email_read(SIMPLE_EMAIL_TEXT)
    assert len(email_object['From'].addresses) == 1
    assert email_object['From'].addresses[0].display_name == 'Bob Bradbury'

    email_object = email_read('foo bar - this is definitely not an email!')
    assert len(email_object.items()) == 0


def test_email_read_odd_line_endings():
    s = """Subject: Buy bitcoin now!\nFrom: Bob Bradbury <bob@gmail.com>\nTo: Alice Asimov <alice@gmail.com>\n\nHi!"""
    email_object = email_read(s)
    assert len(email_object['From'].addresses) == 1
    assert email_object['From'].addresses[0].display_name == 'Bob Bradbury'

    s = """Subject: Buy bitcoin now!\r\nFrom: Bob Bradbury <bob@gmail.com>\r\nTo: Alice Asimov <alice@gmail.com>\r\n\r\nHi!"""
    email_object = email_read(s)
    assert len(email_object['From'].addresses) == 1
    assert email_object['From'].addresses[0].display_name == 'Bob Bradbury'


def test_email_object_new_docs_1():
    assert str(type(email_object_new())) == "<class 'email.message.Message'>"


# def test_email_content_transfer_encoding_docs_1():
#     assert email_content_transfer_encoding(email_text) == 'fill'


def test__is_email_object_docs_1():
    assert not _is_email_object('foo')
    assert _is_email_object(email_object_new())


def test_email_bodies_as_strings_docs_1():
    assert email_bodies_as_strings(SIMPLE_EMAIL_TEXT) == ['Hi!']

    # test a longer email with multiple bodies
    bodies = email_bodies_as_strings(LONG_EMAIL)
    assert len(bodies) == 2
    assert bodies[0].startswith('When you=E2=80=99re')
    assert bodies[1].startswith(
        '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w=\r\n3.org/TR/REC-html40/loose.dtd"><html><head>'
    )


# def test_email_bodies_as_objects_docs_1():
#     assert email_bodies_as_objects(email_text) == 'fill'


def test_email_attachments_docs_1():
    from d8s_networking import get

    email_text = get(
        'https://gist.githubusercontent.com/fhightower/495ca027d72b0870baab6740e7433643/raw/6225a30441e1c899503cc4354566076571a4412a/dummy.eml',
        process_response=True,
    )
    attachments = email_attachments(email_text)
    assert len(attachments) == 2


# def test_email_attachments_objects_docs_1():
#     assert email_attachments_objects(email_text) == 'fill'


def test_email_body_is_base64_docs_1():
    email_text = """Subject: =?UTF-8?B?aGkgYWxpY2UgYXNpbW92?=
From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>
Content-Type: text/html;
    charset="utf-8"
Content-Transfer-Encoding: base64

SSdtIHNvcnJ5IERhdmUsIEknbSBhZnJhaWQgSSBjYW4ndCBkbyB0aGF0

"""
    assert email_body_is_base64(email_text)


def test_email_header_fields_docs_1():
    assert email_header_fields(SIMPLE_EMAIL_TEXT) == ['Subject', 'From', 'To']


# def test_email_headers_docs_1():
#     assert email_headers(email_text) == 'fill'


def test_email_headers_raw_docs_1():
    email_text = """Subject: =?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?=
From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi Alice Asimov!"""
    assert email_headers_raw(email_text) == [
        ('Subject', '=?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?='),
        ('From', 'Bob Bradbury <bob@gmail.com>'),
        ('To', 'Alice Asimov <alice@gmail.com>'),
    ]


# def test_email_headers_as_dict_docs_1():
#     assert email_headers_as_dict(email_text) == 'fill'


def test_email_headers_as_dict_docs_1():
    email_header_json = email_headers_as_dict(SIMPLE_EMAIL_TEXT)
    assert email_header_json == {}

    # test an email with multiple entries for the 'Received' field
    email_text = """Subject: =?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?=
Received: A
Received: B
From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi Alice Asimov!"""
    email_header_json = email_headers_as_dict(SIMPLE_EMAIL_TEXT)
    assert email_header_json == {}


def test_email_header_docs_1():
    assert email_header(SIMPLE_EMAIL_TEXT, 'Subject') == ['Buy bitcoin now!']

    email_text = """Subject: =?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?=
From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi Alice Asimov!"""
    results = email_header(email_text, 'Subject')
    assert results == ['Confirmation Needed: example@gmail.com']

    # test an email with multiple entries for the 'Received' field
    email_text = """Subject: =?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?=
Received: A
Received: B
From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi Alice Asimov!"""
    results = email_header(email_text, 'Received')
    assert results == ['A', 'B']


def test_email_header_delete_field_docs_1():
    assert email_header(SIMPLE_EMAIL_TEXT, 'Subject') == ['Buy bitcoin now!']
    updated_email_object = email_header_delete_field(SIMPLE_EMAIL_TEXT, 'Subject')
    assert email_header(updated_email_object, 'Subject') == None


# def test__email_structure_iterator_docs_1():
#     assert _email_structure_iterator(email_object, email_structure=None) == 'fill'


def test_email_structure_docs_1():
    assert email_structure(SIMPLE_EMAIL_TEXT) == {'type': 'text/plain', 'content_disposition': None, 'children': []}


def test_email_structure_docs_2():
    from d8s_networking import get

    email_text = get(
        'https://gist.githubusercontent.com/fhightower/495ca027d72b0870baab6740e7433643/raw/6225a30441e1c899503cc4354566076571a4412a/dummy.eml',
        process_response=True,
    )

    structure = email_structure(email_text)
    assert structure == {
        'type': 'multipart/mixed',
        'content_disposition': None,
        'children': [
            {
                'type': 'multipart/alternative',
                'content_disposition': None,
                'children': [
                    {'type': 'text/plain', 'content_disposition': None, 'children': []},
                    {'type': 'text/html', 'content_disposition': None, 'children': []},
                ],
            },
            {'type': 'text/xml', 'content_disposition': 'attachment', 'children': []},
            {'type': 'image/png', 'content_disposition': 'attachment', 'children': []},
        ],
    }


def test_email_header_add_raw_docs_1():
    email = '''From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi Alice Asimov!'''
    updated_email_object = email_header_add_raw(
        email, 'Subject', '=?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?='
    )
    assert email_header(updated_email_object, 'Subject') == ['Confirmation Needed: example@gmail.com']


def test_email_header_add_docs_1():
    email = '''From: Bob Bradbury <bob@gmail.com>
To: Alice Asimov <alice@gmail.com>

Hi Alice Asimov!'''
    updated_email_object = email_header_add(
        email, 'Subject', '=?UTF-8?B?Q29uZmlybWF0aW9uIE5lZWRlZDogZXhhbXBsZUBnbWFpbC5jb20=?='
    )
    assert email_header(updated_email_object, 'Subject') == ['Confirmation Needed: example@gmail.com']
