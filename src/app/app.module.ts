import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations'; 
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from "@angular/common/http";
import { RouterModule } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatInputModule } from '@angular/material/input';
import { MatTableModule } from '@angular/material/table';

import { AppComponent } from './app.component';
import { UserInputComponent } from './user-input/user-input/user-input.component';
import { TestComponent } from './test/test.component';
import { SortableModule } from '@progress/kendo-angular-sortable';


@NgModule({
  declarations: [
    AppComponent,
    UserInputComponent,
    TestComponent,
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    RouterModule,
    ReactiveFormsModule,
    MatAutocompleteModule,
    MatInputModule,
    MatTableModule,
    BrowserAnimationsModule,
    SortableModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
