void set_plot_style()
{
    gROOT->ForceStyle();
    const Int_t NRGBs = 5;
    const Int_t NCont = 255;
    Double_t stops[NRGBs] = { 0.00, 0.34, 0.61, 0.84, 1.00 };
    Double_t red[NRGBs]   = { 0.00, 0.00, 0.87, 1.00, 0.51 };
    Double_t green[NRGBs] = { 0.00, 0.81, 1.00, 0.20, 0.00 };
    Double_t blue[NRGBs]  = { 0.51, 1.00, 0.12, 0.00, 0.00 };
    TColor::CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont);
    gStyle->SetNumberContours(NCont);

}

void cmp_f1f2f3()
{
	//COLZ scheme
	set_plot_style();
	TCanvas* c = new TCanvas("canvas","canvas",820,1200);
	c->Divide(2,2);
	//Load trace file
	TFile* f = new TFile("trace123.root");
	TH2F* h1 = (TH2F*)f->FindObjectAny("f1_h4");
	h1->SetTitle("F1");
	h1->GetXaxis()->SetTitle("z (mm)");
	h1->GetYaxis()->SetTitle("y (mm)");
	TH2F* h2 = (TH2F*)f->FindObjectAny("f2_h4");
	h2->SetTitle("F2");
	h2->GetXaxis()->SetTitle("z (mm)");
	h2->GetYaxis()->SetTitle("y (mm)");
	TH2F* h3 = (TH2F*)f->FindObjectAny("f3_h4");
	h3->SetTitle("F3");
	h3->GetXaxis()->SetTitle("z (mm)");
	h3->GetYaxis()->SetTitle("y (mm)");
	c->cd(1);
    	gPad->SetGrid();
	h1->SetMarkerColor(kRed);
	h2->SetMarkerColor(kBlue);
	h3->SetMarkerColor(kBlack);
	h1->Draw("scat");
	h2->Draw("SAME");
	h3->Draw("SAME");
	c->cd(2);
	//h1->SetTitle("Light from F1");
	h1->Draw("COLZ");
	c->cd(3);
	h2->Draw("COLZ");
	c->cd(4);
	h3->Draw("COLZ");
}


void cmp_wire_refl(){
	//COLZ scheme
	set_plot_style();
	TCanvas* c = new TCanvas("canvas","canvas",820,1200);
	c->Divide(2,2);
	//Load trace file
	TFile* f = new TFile("trace123_wire_std.root");
	TH2F* h1 = (TH2F*)f->FindObjectAny("f1_h4");
	h1->SetTitle("F1");
	h1->GetXaxis()->SetTitle("z (mm)");
	h1->GetYaxis()->SetTitle("y (mm)");
	TH2F* h2 = (TH2F*)f->FindObjectAny("f2_h4");
	h2->SetTitle("F2");
	h2->GetXaxis()->SetTitle("z (mm)");
	h2->GetYaxis()->SetTitle("y (mm)");
	TH2F* h3 = (TH2F*)f->FindObjectAny("f3_h4");
	h3->SetTitle("F3");
	h3->GetXaxis()->SetTitle("z (mm)");
	h3->GetYaxis()->SetTitle("y (mm)");
	TFile* g = new TFile("trace123_diff.root");
	TH2F* h4 = (TH2F*)g->FindObjectAny("f1_h4");
	h4->SetTitle("F1");
	h4->GetXaxis()->SetTitle("z (mm)");
	h4->GetYaxis()->SetTitle("y (mm)");
	TH2F* h5 = (TH2F*)g->FindObjectAny("f2_h4");
	h5->SetTitle("F2");
	h5->GetXaxis()->SetTitle("z (mm)");
	h5->GetYaxis()->SetTitle("y (mm)");
	TH2F* h6 = (TH2F*)g->FindObjectAny("f3_h4");
	h6->SetTitle("F3");
	h6->GetXaxis()->SetTitle("z (mm)");
	h6->GetYaxis()->SetTitle("y (mm)");
	h1->SetMarkerColor(kMagenta);
	h2->SetMarkerColor(kMagenta);
	h3->SetMarkerColor(kMagenta);
	h4->SetMarkerColor(kGreen);
	h5->SetMarkerColor(kGreen);
	h6->SetMarkerColor(kGreen);
	c->cd(2);
	gPad->SetGrid();
	h1->Draw("scat");
	h4->Draw("SAME");
	c->cd(3);
	h2->Draw("scat");
	h5->Draw("SAME");
	c->cd(4);
	h3->Draw("scat");
	h6->Draw("SAME");

}
