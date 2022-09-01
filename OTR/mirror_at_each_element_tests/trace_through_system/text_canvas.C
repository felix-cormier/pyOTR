#include <iostream>
#include <fstream>
#include <string>
using namespace std;

void canvas(){
    fstream newfile;
    newfile.open("textfile.txt",ios::in);
    string text[3];
    if(newfile.is_open()){
    	string tp;
	int i = 0;
	while(getline(newfile,tp)){
		cout << tp << "\n";
		text[i] = tp;
		cout << text[i] << "\n";
		i++;
	}
	newfile.close();
    }

    TCanvas *c1 = new TCanvas("c1","Canvas Example",200,10,600,480);  
    gBenchmark->Start("canvas");
    // Inside this canvas, we create two pads
    TPad *pad1 = new TPad("pad1","This is pad1",0.25,0.25,0.75,0.75);
    pad1->SetFillColor(11);
    pad1->Draw();  
    pad1->cd();
    TLatex *t1 = new TLatex(0.2,0.8,Form("#theta = %s",text[0].c_str()));
    TLatex *t2 = new TLatex(0.2,0.6,Form("#hat{#sigma} = %s",text[1].c_str()));
    TLatex *t3 = new TLatex(0.2,0.4,Form("#hat{#varepsilon} = %s",text[2].c_str()));
    t1->SetTextFont(23);
    t1->SetTextSize(40); 
    t2->SetTextFont(23);
    t2->SetTextSize(40); 
    t3->SetTextFont(23);
    t3->SetTextSize(40); 
    t1->Draw();
    t2->Draw();
    t3->Draw();

    // A pad may contain other pads and graphics objects.
    // We set the current pad to pad2.
    // Note that the current pad is always highlighted.
//    pad2->cd();
//    TPad *pad21 = new TPad("pad21","First subpad of pad2",0.02,0.05,0.48,0.95,17,3);
//    TPad *pad22 = new TPad("pad22","Second subpad of pad2",0.52,0.05,0.98,0.95,17,3);
//    pad21->Draw();
//    pad22->Draw();
//  
//    // We enter some primitives in the created pads and set some attributes
//    pad1->cd();
//    float xt1 = 0.5;
//    float yt1 = 0.1;
//    TText *t1 = new TText(0.5,yt1,"ROOT");
//    t1->SetTextAlign(22);
//    t1->SetTextSize(0.05);
//    t1->Draw();
//    TLine *line1 = new TLine(0.05,0.05,0.80,0.70);
//    line1->SetLineWidth(8);
//    line1->SetLineColor(2);
//    line1->Draw();
//    line1->DrawLine(0.6,0.1,0.9,0.9);
//    TLine *line2 = new TLine(0.05,0.70,0.50,0.10);
//    line2->SetLineWidth(4);
//    line2->SetLineColor(5);
//    line2->Draw();
//  
//    pad21->cd();
//    TText *t21 = new TText(0.05,0.8,"This is pad21");
//    t21->SetTextSize(0.1);
//    t21->Draw();
//    float xp2 = 0.5;
//    float yp2 = 0.4;
//    TPavesText *paves = new TPavesText(0.1,0.1,xp2,yp2);
//    paves->AddText("This is a PavesText");
//    paves->AddText("You can add new lines");
//    paves->AddText("Text formatting is automatic");
//    paves->SetFillColor(43);
//    paves->Draw();
//    pad22->cd();
//    TText *t22 = new TText(0.05,0.8,"This is pad22");
//    t22->SetTextSize(0.1);
//    t22->Draw();
//    float xlc = 0.01;
//    float ylc = 0.01;
//    TPaveLabel *label = new TPaveLabel(xlc, ylc, xlc+0.8, ylc+0.1,"This is a PaveLabel");
//    label->SetFillColor(24);
//    label->Draw();
//  
//    // Modify object attributes in a loop
//    Int_t nloops = 50;
//    float dxp2   = (0.9-xp2)/nloops;
//    float dyp2   = (0.7-yp2)/nloops;
//    float dxlc   = (0.1-xlc)/nloops;
//    float dylc   = (0.4-xlc)/nloops;
//    float dxt1   = (0.5-xt1)/nloops;
//    float dyt1   = (0.8-yt1)/nloops;
//    float t10    = t1->GetTextSize();
//    float t1end  = 0.3;
//    float t1ds   = (t1end - t10)/nloops;
//    Int_t color  = 0;
//    for (int i=0;i<nloops;i++) {
//       color++;
//       color %= 8;
//       line1->SetLineColor(color);
//       t1->SetTextSize(t10 + t1ds*i);
//       t1->SetTextColor(color);
//       t1->SetX(xt1+dxt1*i);
//       t1->SetY(yt1+dyt1*i);
//       pad1->Modified();
//       paves->SetX2NDC(xp2+dxp2*i);
//       paves->SetY2NDC(yp2+dyp2*i);
//       pad21->Modified();
//       label->SetX1NDC(xlc+dxlc*i);
//       label->SetY1NDC(ylc+dylc*i);
//       label->SetX2NDC(xlc+dxlc*i+0.8);
//       label->SetY2NDC(ylc+dylc*i+0.2);
//       pad22->Modified();
//       c1->Update();
//    }
//   gBenchmark->Show("canvas");
 }

