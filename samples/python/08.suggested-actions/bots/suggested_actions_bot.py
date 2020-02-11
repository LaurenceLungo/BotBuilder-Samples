# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import json
import os.path
from botbuilder.core import ActivityHandler, MessageFactory, CardFactory, TurnContext
from botbuilder.schema import ChannelAccount, CardAction, ActionTypes, SuggestedActions
from botbuilder.schema import (
    ChannelAccount,
    HeroCard,
    CardAction,
    CardImage,
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity,
    ActionTypes,
)

uninit = "uninit"
reserve = "reserve"
order = "order"
check = "check"
queue = "queue"
cancel = "cancel"
start_over = "start over"

menu = [ 
            CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static7.orstatic.com/userphoto/photo/A/8B4/01N36I8D34B9EA6A565DABpx.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="餐蛋治",
                        display_text="餐蛋治",
                        text="餐蛋治",
                        value="餐蛋治"
                    )
                ],
            )),
            CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static6.orstatic.com/userphoto2/photo/18/YVS/06W2114A573530B4715387px.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="叉燒通粉",
                        display_text="叉燒通粉",
                        text="叉燒通粉",
                        value="叉燒通粉"
                    )
                ],
            )),
            CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static5.orstatic.com/userphoto/photo/E/BNN/02AW5CD60080AEED76A1A5px.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="奶茶",
                        display_text="奶茶",
                        text="奶茶",
                        value="奶茶"
                    )
                ],
            )),
            CardFactory.hero_card(HeroCard(
                title="",
                images=[
                    CardImage(
                        url="https://static8.orstatic.com/userphoto/photo/3/2E9/00H1CBA0F892888F0BF8E0px.jpg"
                    )
                ],
                buttons=[
                    CardAction(
                        type=ActionTypes.message_back,
                        title="凍檸茶",
                        display_text="凍檸茶",
                        text="凍檸茶",
                        value="凍檸茶"
                    )
                ],
            ))
        ]
class SuggestActionsBot(ActivityHandler):
    uninit = "uninit"
    reserve = "reserve"
    order = "order"
    check = "check"
    cancel = "cancel"
    start_over = "start over"

    context = uninit
    class reservation_profile:
        date_time=None
        num=None
    
    class queue_profile:
        pos=None

    """
    This bot will respond to the user's input with suggested actions.
    Suggested actions enable your bot to present buttons that the user
    can tap to provide input.
    """

    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        """
        Send a welcome message to the user and tell them what actions they may perform to use this bot
        """

        return await self._send_welcome_message(turn_context)

    async def on_message_activity(self, turn_context: TurnContext):
        """
        Respond to the users choice and display the suggested actions again.
        """
        print("\n turn_context", turn_context.activity)
        text = ''
        if turn_context.activity.text:
            text = turn_context.activity.text.lower()
        else:
            text = turn_context.activity.value
        
        print("\n text", text)
        response_text = self._process_input(text)

        for i in response_text:
            if i == 505:
                await turn_context.send_activity(MessageFactory.text("What else can I do for you?"))
                await self._send_suggested_actions(turn_context)
            elif i == 606:
                await turn_context.send_activity(MessageFactory.attachment(self.create_adaptive_card_attachment()))
            else:
                await turn_context.send_activity(i)

        # return await self._send_suggested_actions(turn_context)

    async def _send_welcome_message(self, turn_context: TurnContext):
        for member in turn_context.activity.members_added:
            if member.id != turn_context.activity.recipient.id:
                # await turn_context.send_activity(
                #     MessageFactory.text(
                #         "Welcome to 澳洲牛奶公司! I'm SmartServe, your waiter today. How can I help you?"
                #     )
                # )

                await turn_context.send_activity(MessageFactory.attachment(self.create_adaptive_card_attachment()))
                # await self._send_suggested_actions(turn_context)

    def _process_input(self, text: str):
        response = []

        if text == cancel:
            self.context = uninit
            response.append(505)
            return response

        elif text == start_over:
            self.context = uninit
            response.append(606)
            return response

        elif text == reserve:
            self.context = reserve
            response.append(MessageFactory.text("How many people will there be?"))
            return response

        elif text == order:
            self.context = order
            response.append(MessageFactory.text("Please take a look at our menu~"))
            response.append(MessageFactory.carousel(menu))
            return response

        elif text == queue:
            self.context = queue
            response.append(MessageFactory.text("Table for?"))
            return response

        elif text == check:
            self.context = "blue"
            response.append(MessageFactory.text("Sure, here is your bill."))
            response.append(MessageFactory.text("Total: HKD49"))
            response.append(MessageFactory.text("Thanks for dining in 澳洲牛奶公司! Hope to see you again soon!"))
            return response

        elif self.context == order:
            if text == "餐蛋治" or text == "叉燒通粉" or text == "奶茶" or text == "凍檸茶":
                response.append(MessageFactory.text("Sure thing! Your order has been placed."))
                response.append(505)
                return response
        elif self.context == reserve:
            if text.isdigit():
                self.reservation_profile.num = text
                response.append(MessageFactory.text("Get it, so what date and time are you booking for?"))
                return response
            else:
                self.reservation_profile.date_time = text
                response.append(MessageFactory.text("All done! A table of "+self.reservation_profile.num+" people is reserved for you on "+self.reservation_profile.date_time+"."))
                response.append(505)
                return response
        
        elif self.context == queue:
            if text.isdigit():
                self.queue_profile.pos = text
                response.append(MessageFactory.text("Your ticket: C4"))
                response.append(MessageFactory.text("Current queue position: 3"))
                response.append(505)
                return response

        response.append(MessageFactory.text("Sorry, I don't understand... Can you repeat again?"))
        return response

    async def _send_suggested_actions(self, turn_context: TurnContext):
        """
        Creates and sends an activity with suggested actions to the user. When the user
        clicks one of the buttons the text value from the "CardAction" will be displayed
        in the channel just as if the user entered the text. There are multiple
        "ActionTypes" that may be used for different situations.
        """

        reply = MessageFactory.text("")

        reply.suggested_actions = SuggestedActions(
            actions=[
                CardAction(title="Reserve a table", type=ActionTypes.im_back, value=reserve),
                CardAction(title="Get a queue ticket", type=ActionTypes.im_back, value=queue),
                CardAction(title="Take an order", type=ActionTypes.im_back, value=order),
                CardAction(title="Check the bill", type=ActionTypes.im_back, value=check)
            ]
        )

        return await turn_context.send_activity(reply)

    def create_adaptive_card_attachment(self):
        relative_path = os.path.abspath(os.path.dirname(__file__))
        path = os.path.join(relative_path, "../cards/welcomeCard.json")
        with open(path) as in_file:
            card = json.load(in_file)

        return Attachment(
            content_type="application/vnd.microsoft.card.adaptive", content=card
        )
