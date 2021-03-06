from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest


class RecipeCreateTest(FunctionalTest):

    def test_can_add_a_recipe(self):
        # Ben goes to the recipe website homepage
        self.browser.get(self.server_url)

        # He notices the page title mention cookbook
        self.assertIn('cookbook', self.browser.title)

        # He is invited to enter his name to create his own cookbook or
        # view other user's cookbook's
        # Ben wants to create his own right now, so he enters his name
        # and then clicks the 'get started button'
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('Ben')
        username_input.send_keys(Keys.ENTER)

        # Ben goes to a unique URL which includes his name
        ben_url = self.browser.current_url
        self.assertRegex(ben_url, '/users/ben.+')

        # He is invited to click on a link to add a new recipe
        add_recipe_button = self.browser.find_element_by_id('id_add_recipe_button')
        self.assertIn('Add recipe', add_recipe_button.text)

        # He clicks on the link and new page appears
        add_recipe_button.click()

        # When he adds a new recipe, he is taken to a new URL
        self.assertRegex(self.browser.current_url, '/users/.*/add_recipe')

        # He sees a form with a textbox for name, ingredients, directions and servings
        # along with a 'cancel' and 'add' button
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Add Recipe', header_text)
        name_textbox = self.browser.find_element_by_id('id_title')
        self.assertEqual(name_textbox.get_attribute('placeholder'),
                         'Enter the title of the recipe')
        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        directions_textbox = self.browser.find_element_by_id('id_directions')
        servings_textbox = self.browser.find_element_by_id('id_servings')
        source_textbox = self.browser.find_element_by_id('id_source')
        source_url_textbox = self.browser.find_element_by_id('id_source_url')
        img_url_textbox = self.browser.find_element_by_id('id_img_url')
        cooking_time_textbox = self.browser.find_element_by_id('id_cooking_time')
        total_time_textbox = self.browser.find_element_by_id('id_total_time')
        notes_textbox = self.browser.find_element_by_id('id_notes')
        add_button = self.browser.find_element_by_id('id_add_button')

        # He types in Grilled Halibut with Mango-Avocado Salsa into the textbox for name
        name_textbox.send_keys('Grilled Halibut with Mango-Avocado Salsa')

        # He types in ingredients:
        ingredients_textbox.send_keys('1 medium ripe avocado, peeled and cut into 1/2" dice')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('1 medium ripe mango, peeled and cut into 1/2" dice')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('1 cup cherry tomatoes, quartered')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('4 large fresh basil leaves, thinly sliced')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('3 tablespoons extra-virgin olive oil, divided, plus more for brushing')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('3 tablespoons fresh lime juice, divided')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('Kosher salt and freshly ground black pepper')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('4 6-ounce halibut or mahi-mahi fillets')
        ingredients_textbox.send_keys(Keys.ENTER)
        ingredients_textbox.send_keys('4 lime wedges')

        # He then types in the following for directions:
        directions_textbox.send_keys('Prepare a grill to medium-high heat. Gently combine the avocado, mango, '
                                     'tomatoes, basil, 1 tablespoon oil, and 1 tablespoon lime juice in a large mixing '
                                     'bowl. Season salsa to taste with salt and pepper and set aside at room '
                                     'temperature, gently tossing occasionally.')
        directions_textbox.send_keys(Keys.ENTER)
        directions_textbox.send_keys('Place fish fillets in a 13x9x2" glass baking dish. Drizzle remaining 2 '
                                     'tablespoon oil and 2 tablespoon lime juice over. Season fish with salt and '
                                     'pepper. Let marinate at room temperature for  10 minutes, turning fish '
                                     'occasionally.')
        directions_textbox.send_keys(Keys.ENTER)
        directions_textbox.send_keys('Brush grill rack with oil. Grill fish until just opaque in center, about 5 '
                                     'minutes per side. Transfer to plates. Spoon mango-avocado salsa over fish. '
                                     'Squeeze a lime wedge over each and serve.')

        # He then types in the servings
        servings_textbox.send_keys('4')

        source_textbox.send_keys('Bon Appetit')
        source_url_textbox.send_keys('http://www.bonappetit.com/recipe/gwyneth-paltrow-s-grilled-halibut-with-mango-avocado-salsa')
        img_url_textbox.send_keys('http://www.bonappetit.com/wp-content/uploads/2010/05/gwyneth-paltrow-s-grilled-halibut-with-mango-avocado-salsa-940x600.jpg')
        cooking_time_textbox.send_keys('10 mins')
        total_time_textbox.send_keys('25 mins')
        notes_textbox.send_keys('Typically use Mahi instead')

        # Finally, he clicks the add button
        add_button.click()

        # He is returned to the main page

        # He sees that the recipe appears in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')

        # He clicks on the recipe that he just added to verify the content
        recipe_link = self.browser.find_element_by_link_text('Grilled Halibut with Mango-Avocado Salsa')
        recipe_link.click()
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('4 6-ounce halibut or mahi-mahi fillets', page_text)
        self.assertIn('Typically use Mahi instead', page_text)

        # he then clicks the back button to go back
        back_button = self.browser.find_element_by_id('id_back_button')
        self.assertIn('Back', back_button.text)
        back_button.click()

        # He then goes to add another recipe
        add_recipe_button = self.browser.find_element_by_id('id_add_recipe_button')
        add_recipe_button.click()

        # He then goes to add yet another recipe
        # He sees a form with a textbox for name, ingredients, directions and servings
        # along with a 'cancel' and 'add' button
        name_textbox = self.browser.find_element_by_id('id_title')
        add_button = self.browser.find_element_by_id('id_add_button')
        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        directions_textbox = self.browser.find_element_by_id('id_directions')

        # He types in Grilled Halibut with Mango-Avocado Salsa into the textbox for name
        name_textbox.send_keys('Yogurt-Marinated Grilled Chicken')
        ingredients_textbox.send_keys('yogurt')
        directions_textbox.send_keys('grill')
        add_button.click()

        # He sees that both recipes appear in the list of recipes
        self.check_for_row_in_list_table('Grilled Halibut with Mango-Avocado Salsa')
        self.check_for_row_in_list_table('Yogurt-Marinated Grilled Chicken')

        # He closes his browser
        self.browser.quit()
        # Note: we use a new instance of Firefox to make sure no information from cookies
        # is bleeding through
        self.browser = webdriver.Firefox()

        # Sarah visits the home page and enters her name.
        self.browser.get(self.server_url)
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys('Sarah')
        username_input.send_keys(Keys.ENTER)

        # Sarah gets her own unique URL
        sarah_url = self.browser.current_url
        self.assertRegex(sarah_url, '/users/sarah.+')
        self.assertNotEqual(sarah_url, ben_url)

        # There is no sign of Ben's items
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Grilled Halibut with Mango-Avocado Salsa', page_text)
        self.assertNotIn('Yogurt-Marinated Grilled Chicken', page_text)

        # Sarah then adds a recipe
        add_recipe_button = self.browser.find_element_by_id('id_add_recipe_button')
        add_recipe_button.click()

        name_textbox = self.browser.find_element_by_id('id_title')
        add_button = self.browser.find_element_by_id('id_add_button')
        ingredients_textbox = self.browser.find_element_by_id('id_ingredients')
        directions_textbox = self.browser.find_element_by_id('id_directions')
        name_textbox.send_keys('Beer Braised Bratwurst')
        ingredients_textbox.send_keys('beer')
        directions_textbox.send_keys('braise')
        add_button.click()

        # There is still no sign of Ben's recipes
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Grilled Halibut with Mango-Avocado Salsa', page_text)
        self.assertNotIn('Yogurt-Marinated Grilled Chicken', page_text)

        # She closes his browser
        self.browser.quit()
        # Note: we use a new instance of Firefox to make sure no information from cookies
        # is bleeding through
        self.browser = webdriver.Firefox()

        # Ben checks if he can go back to his URL
        # He then reopens his browser and sees that the recipe that he added is still there
        self.browser.get(ben_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Grilled Halibut with Mango-Avocado Salsa', page_text)
        self.assertIn('Yogurt-Marinated Grilled Chicken', page_text)

        # Ben goes back to the recipe home site
        self.browser.get(self.server_url)
        # He notices that Ben's and Sarah's cookbooks are listed
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Ben', page_text)
        self.assertIn('Sarah', page_text)
        ben_cookbook_link = self.browser.find_element_by_link_text("Ben")
        ben_cookbook_link.click()
        # He clicks the link for his cookbook and notices it is the same as his URL from before
        self.assertEqual(self.browser.current_url, ben_url)
        # He sees his two recipes that he added earlier
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertIn('Grilled Halibut with Mango-Avocado Salsa', page_text)
        self.assertIn('Yogurt-Marinated Grilled Chicken', page_text)
