import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MatTableDataSource } from '@angular/material';
import { FormControl } from '@angular/forms';
//import { SortablejsModule } from 'angular-sortablejs';

@Component({
  selector: 'app-user-input',
  templateUrl: './user-input.component.html',
  encapsulation: ViewEncapsulation.None,
  styleUrls: ['./user-input.component.css']
})
export class UserInputComponent{
  title = 'app';
  // for Autocomplete
  myControl: FormControl = new FormControl();

  options = [];
  //suggestionResultJson: string[];
  //suggestionResultJson2: string[];
  suggestionResultDC: string[];
  suggestionResultRelatedF: string[];
  suggestionResultRiskF: string[];

  //serverData: JSON;
  response: JSON;
  keyword: string = "";

  //keywordAlter: string = "";
  keywordDC: string = "";
  keywordRelatedF: string = "";
  keywordRiskF: string = "";

  //keywordAlterAll: string = "";
  keywordDefiningChar: string = "";
  keywordRelatedFactor: string = "";
  keywordRiskFactor: string = "";
  
  tempKeywordAlter: string = "";
  tempResponse :JSON;
  keywordHistorys: string;
  keywordHistorysJson: JSON;
  keywordHistoryQueried = false;
  searchResult: string[];
  searchTermCharResult: JSON;
  isSeachFactor = false;
  selected = [1,2,3];


  constructor(private httpClient: HttpClient) {
    // this.httpClient.get('http://127.0.0.1:5002/keywordhistory').subscribe(data => {
    //   this.keywordHistorys = data as string;
    //   this.keywordHistorysJson = JSON.parse(this.keywordHistorys)
    //   this.keywordHistoryQueried = true;
    // })
    this.httpClient.get('http://127.0.0.1:5002/suggestion?keyword=a').subscribe(data => {
      this.suggestionResultDC = data as string[];
      this.suggestionResultRelatedF = data as string[];
      this.suggestionResultRiskF = data as string[];
      //console.log(this.suggestionResultJson[300])
      //this.suggestionResultJson = ["one","two","three"];
    })
  }

  ngOnInit() {
    
  }

  test() {
    this.keyword = "123";
  }

  // getSuggestion() {
  //   this.httpClient.get('http://127.0.0.1:5002/suggestion?keyword='+this.keyword).subscribe(data => {
  //     this.suggestionResultJson = data as string[];
  //   })
  // }
  getSuggestionDC() {
    if(this.keywordDC.includes(";")){
      this.keywordDefiningChar += this.keywordDC;
      this.keywordDC = "";
    }
    //this.tempKeywordAlter = this.keywordAlter.split("1").slice(-1)[0].trim()
    this.httpClient.get('http://127.0.0.1:5002/suggestion?keyword='+this.keywordDC).subscribe(data => {
      this.suggestionResultDC = data as string[];
    })
  }
  getSuggestionRelatedF() {
    if(this.keywordRelatedF.includes(";")){
      this.keywordRelatedFactor += this.keywordRelatedF;
      this.keywordRelatedF = "";
    }
    //this.tempKeywordAlter = this.keywordAlter.split("1").slice(-1)[0].trim()
    this.httpClient.get('http://127.0.0.1:5002/suggestion?keyword='+this.keywordRelatedF).subscribe(data => {
      this.suggestionResultRelatedF = data as string[];
    })
  }
  getSuggestionRiskF() {
    if(this.keywordRiskF.includes(";")){
      this.keywordRiskFactor += this.keywordRiskF;
      this.keywordRiskF = "";
    }
    //this.tempKeywordAlter = this.keywordAlter.split("1").slice(-1)[0].trim()
    this.httpClient.get('http://127.0.0.1:5002/suggestion?keyword='+this.keywordRiskF).subscribe(data => {
      this.suggestionResultRiskF = data as string[];
    })
  }

  queryResult() {
    this.httpClient.get(
      'http://127.0.0.1:5002/?keyworddc='+this.keywordDefiningChar+'&keywordrelatedf='+this.keywordRelatedFactor+'&keywordriskf='+this.keywordRiskFactor
    ).subscribe(data => {
      this.searchResult = data as string[];
    })
    // this.httpClient.get('http://127.0.0.1:5002/keywordhistory').subscribe(data => {
    //   this.keywordHistorys = data as string;
    //   this.keywordHistorysJson = JSON.parse(this.keywordHistorys);
    //   this.keywordHistoryQueried = true;
    // })
  }
  historyQueryResult(keyword) {
    this.httpClient.get('http://127.0.0.1:5002/?keyword='+keyword).subscribe(data => {
      this.searchResult = data as string[];
    })
    this.httpClient.get('http://127.0.0.1:5002/keywordhistory').subscribe(data => {
      this.keywordHistorys = data as string;
      this.keywordHistorysJson = JSON.parse(this.keywordHistorys)
      this.keywordHistoryQueried = true;
    })
  }
  searchCUI(keyword) {
    
  }

  getKeywordHistory() {
    this.httpClient.get('http://127.0.0.1:5002/keywordhistory').subscribe(data => {
      this.keywordHistorys = data as string;
      this.keywordHistorysJson = JSON.parse(this.keywordHistorys)
      this.keywordHistoryQueried = true;
    })
  }

  getFactor(name, code) {
    this.httpClient.get('http://127.0.0.1:5002/getfactor?name='+name+'&code='+code).subscribe(data => {
      this.searchTermCharResult = data as JSON;
      this.isSeachFactor = true;
    })
  }

  select(keyword: string){
    this.selected.push(keyword);
  }
}